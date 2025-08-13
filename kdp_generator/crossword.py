import random
from typing import List, Tuple, Dict, Optional, Set
import os

from reportlab.lib.colors import black, white
from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

GRID_SIZE = 10


def load_wordlist(language: str) -> List[str]:
    base_dir = os.path.join(os.path.dirname(__file__), "wordlists")
    filename = "english.txt" if language.lower().startswith("en") else "polish.txt"
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        words = [w.strip().upper() for w in f if w.strip() and w.strip().isalpha()]
    # prefer 3-8 letters for better fit
    words = [w for w in words if 3 <= len(w) <= 8]
    random.shuffle(words)
    return words


def can_place(grid: List[List[str]], word: str, r: int, c: int, direction: str, require_overlap: bool) -> bool:
    dr, dc = (0, 1) if direction == 'A' else (1, 0)
    if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
        return False
    r2 = r + dr * (len(word) - 1)
    c2 = c + dc * (len(word) - 1)
    if not (0 <= r2 < GRID_SIZE and 0 <= c2 < GRID_SIZE):
        return False
    overlap = False
    for i, ch in enumerate(word):
        rr = r + dr * i
        cc = c + dc * i
        cell = grid[rr][cc]
        if cell not in ('.', ch):
            return False
        if cell == ch:
            overlap = True
    if require_overlap and not overlap:
        return False
    # Ensure adjacent cells do not create two-letter touching (simple rule)
    # Check before and after the word
    br, bc = r - dr, c - dc
    ar, ac = r2 + dr, c2 + dc
    if 0 <= br < GRID_SIZE and 0 <= bc < GRID_SIZE and grid[br][bc].isalpha():
        return False
    if 0 <= ar < GRID_SIZE and 0 <= ac < GRID_SIZE and grid[ar][ac].isalpha():
        return False
    # Check side-adjacency along the word
    for i in range(len(word)):
        rr = r + dr * i
        cc = c + dc * i
        # perpendicular neighbors
        if direction == 'A':
            for nr in (rr - 1, rr + 1):
                if 0 <= nr < GRID_SIZE and grid[nr][cc].isalpha():
                    if grid[rr][cc] == '.':
                        return False
        else:
            for nc in (cc - 1, cc + 1):
                if 0 <= nc < GRID_SIZE and grid[rr][nc].isalpha():
                    if grid[rr][cc] == '.':
                        return False
    return True


def place_word(grid: List[List[str]], word: str, r: int, c: int, direction: str):
    dr, dc = (0, 1) if direction == 'A' else (1, 0)
    for i, ch in enumerate(word):
        rr = r + dr * i
        cc = c + dc * i
        grid[rr][cc] = ch


def generate_crossword(language: str = "pl") -> Tuple[List[List[str]], List[str]]:
    # Start with empty grid
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    words = load_wordlist(language)

    used: List[str] = []
    placed_any = False

    # Place first word in the middle horizontally for better anchoring
    for w in words[:]:
        if len(w) <= GRID_SIZE:
            r = GRID_SIZE // 2
            c = max(0, (GRID_SIZE - len(w)) // 2)
            if can_place(grid, w, r, c, 'A', require_overlap=False):
                place_word(grid, w, r, c, 'A')
                used.append(w)
                words.remove(w)
                placed_any = True
                break

    # Place remaining words trying to overlap
    for w in words:
        placed = False
        # Try to place with overlap preference
        positions: List[Tuple[int, int, str]] = []
        # Heuristic: try across first then down, random order
        dirs = ['A', 'D']
        random.shuffle(dirs)
        for direction in dirs:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if can_place(grid, w, r, c, direction, require_overlap=True):
                        positions.append((r, c, direction))
        random.shuffle(positions)
        for (r, c, direction) in positions:
            place_word(grid, w, r, c, direction)
            used.append(w)
            placed = True
            break
        if not placed:
            # as a fallback allow placement without overlap if grid is very sparse
            if sum(ch.isalpha() for row in grid for ch in row) < 10:
                tries = [(random.randrange(GRID_SIZE), random.randrange(GRID_SIZE), random.choice(['A', 'D'])) for _ in range(50)]
                for r, c, direction in tries:
                    if can_place(grid, w, r, c, direction, require_overlap=False):
                        place_word(grid, w, r, c, direction)
                        used.append(w)
                        placed = True
                        break
        # stop if enough words
        if len(used) >= 18:
            break

    # Convert non-letter cells to blocks '#'
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if not grid[r][c].isalpha():
                grid[r][c] = '#'

    if not used:
        raise RuntimeError("Could not place words for crossword. Try again with another language or update wordlist.")

    return grid, used


def render_crossword_pdf(grid: List[List[str]], filename: str, trim_size: str = "8.5x11", words: Optional[List[str]] = None):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    grid_size = min(page_width, page_height) - 2 * margin
    cell_size = grid_size / GRID_SIZE
    origin_x = (page_width - grid_size) / 2
    origin_y = (page_height - grid_size) / 2

    canvas.setLineWidth(1.5)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            x = origin_x + c * cell_size
            y = origin_y + (GRID_SIZE - 1 - r) * cell_size
            if grid[r][c] == '#':
                canvas.setFillColor(black)
                canvas.rect(x, y, cell_size, cell_size, fill=1, stroke=0)
            else:
                canvas.setFillColor(white)
                canvas.rect(x, y, cell_size, cell_size, fill=1, stroke=1)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()

    if words:
        canvas.setFont("Helvetica-Bold", 20)
        title = "Word List"
        tw = canvas.stringWidth(title, "Helvetica-Bold", 20)
        canvas.drawString((page_width - tw) / 2, page_height - margin - 20, title)
        canvas.setFont("Helvetica", 12)
        col_w = (page_width - 2 * margin) / 3
        x0 = margin
        y = page_height - margin - 50
        line_h = 16
        col = 0
        for w in sorted(words):
            canvas.drawString(x0 + col * col_w, y, w)
            y -= line_h
            if y < margin + 20:
                col += 1
                y = page_height - margin - 50
                if col > 2:
                    canvas.showPage()
                    draw_footer_page_number(canvas, page_width, margin, 2)
                    canvas.setFont("Helvetica", 12)
                    col = 0
        draw_footer_page_number(canvas, page_width, margin, 2)
        canvas.showPage()

    canvas.save()


def render_crossword_book_pdf(grids: List[List[List[str]]], filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    grid_draw = min(page_width, page_height) - 2 * margin
    cell_size = grid_draw / GRID_SIZE
    origin_x = (page_width - grid_draw) / 2
    origin_y = (page_height - grid_draw) / 2

    page_num = 1
    for grid in grids:
        canvas.setLineWidth(1.5)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = origin_x + c * cell_size
                y = origin_y + (GRID_SIZE - 1 - r) * cell_size
                if grid[r][c] == '#':
                    canvas.setFillColor(black)
                    canvas.rect(x, y, cell_size, cell_size, fill=1, stroke=0)
                else:
                    canvas.setFillColor(white)
                    canvas.rect(x, y, cell_size, cell_size, fill=1, stroke=1)
        draw_footer_page_number(canvas, page_width, margin, page_num)
        canvas.showPage()
        page_num += 1
    canvas.save()