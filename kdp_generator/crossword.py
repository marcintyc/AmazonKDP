import random
from typing import List, Tuple, Dict, Optional
import os

GRID_SIZE = 10

# Predefined symmetric block patterns for 10x10 ("#" is block, "." is fill)
BLOCK_PATTERNS = [
    [
        "..#..#..#.",
        "..#..#..#.",
        "#########.",
        "..#..#..#.",
        "..#..#..#.",
        "..#..#..#.",
        "#########.",
        "..#..#..#.",
        "..#..#..#.",
        "..#..#..#.",
    ],
    [
        "#..#..#..#",
        "..........",
        "#..#..#..#",
        "..........",
        "#..#..#..#",
        "..........",
        "#..#..#..#",
        "..........",
        "#..#..#..#",
        "..........",
    ],
    [
        "..#...#...",
        "..#...#...",
        "########..",
        "...#...#..",
        "...#...#..",
        "..#...#...",
        "..########",
        "...#...#..",
        "...#...#..",
        "..#...#...",
    ],
]


def load_wordlist(language: str) -> List[str]:
    base_dir = os.path.join(os.path.dirname(__file__), "wordlists")
    filename = "english.txt" if language.lower().startswith("en") else "polish.txt"
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        words = [w.strip().upper() for w in f if w.strip() and w.strip().isalpha()]
    # limit to words 3-10 letters
    return [w for w in words if 3 <= len(w) <= GRID_SIZE]


def find_slots(pattern: List[str]) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    # Returns (across_slots, down_slots), each slot is (row, col, length)
    across = []
    for r in range(GRID_SIZE):
        c = 0
        while c < GRID_SIZE:
            if pattern[r][c] != '#':
                start = c
                while c < GRID_SIZE and pattern[r][c] != '#':
                    c += 1
                length = c - start
                if length >= 3:
                    across.append((r, start, length))
            else:
                c += 1
    down = []
    for c in range(GRID_SIZE):
        r = 0
        while r < GRID_SIZE:
            if pattern[r][c] != '#':
                start = r
                while r < GRID_SIZE and pattern[r][c] != '#':
                    r += 1
                length = r - start
                if length >= 3:
                    down.append((start, c, length))
            else:
                r += 1
    return across, down


def can_place(grid: List[List[str]], word: str, r: int, c: int, length: int, direction: str) -> bool:
    if len(word) != length:
        return False
    if direction == 'A':
        for i in range(length):
            ch = grid[r][c + i]
            if ch == '#':
                return False
            if ch != '.' and ch != word[i]:
                return False
    else:
        for i in range(length):
            ch = grid[r + i][c]
            if ch == '#':
                return False
            if ch != '.' and ch != word[i]:
                return False
    return True


def place_word(grid: List[List[str]], word: str, r: int, c: int, direction: str) -> List[Tuple[int, int]]:
    changed = []
    if direction == 'A':
        for i, ch in enumerate(word):
            if grid[r][c + i] == '.':
                grid[r][c + i] = ch
                changed.append((r, c + i))
    else:
        for i, ch in enumerate(word):
            if grid[r + i][c] == '.':
                grid[r + i][c] = ch
                changed.append((r + i, c))
    return changed


def undo_changes(grid: List[List[str]], changes: List[Tuple[int, int]]):
    for r, c in changes:
        grid[r][c] = '.'


def build_grid(pattern: List[str]) -> List[List[str]]:
    grid = []
    for r in range(GRID_SIZE):
        row = []
        for c in range(GRID_SIZE):
            row.append('#' if pattern[r][c] == '#' else '.')
        grid.append(row)
    return grid


def get_constraints_for_slot(grid: List[List[str]], r: int, c: int, length: int, direction: str) -> str:
    letters = []
    if direction == 'A':
        for i in range(length):
            letters.append(grid[r][c + i])
    else:
        for i in range(length):
            letters.append(grid[r + i][c])
    return ''.join(letters)


def filter_words(words_by_len: Dict[int, List[str]], pattern: str) -> List[str]:
    candidates = []
    for w in words_by_len.get(len(pattern), []):
        ok = True
        for i, ch in enumerate(pattern):
            if ch != '.' and ch != w[i]:
                ok = False
                break
        if ok:
            candidates.append(w)
    random.shuffle(candidates)
    return candidates


def backtrack_fill(grid: List[List[str]], slots: List[Tuple[int, int, int, str]], words_by_len: Dict[int, List[str]], used: set) -> bool:
    if not slots:
        return True
    # Choose the slot with most constraints (fewest candidates)
    best_idx = None
    best_candidates = None
    for idx, (r, c, length, direction) in enumerate(slots):
        pattern = get_constraints_for_slot(grid, r, c, length, direction)
        candidates = [w for w in filter_words(words_by_len, pattern) if w not in used]
        if best_candidates is None or len(candidates) < len(best_candidates):
            best_candidates = candidates
            best_idx = idx
        if best_candidates is not None and len(best_candidates) == 0:
            break
    if best_candidates is None or len(best_candidates) == 0:
        return False
    (r, c, length, direction) = slots[best_idx]
    remaining = slots[:best_idx] + slots[best_idx + 1:]
    for word in best_candidates:
        if can_place(grid, word, r, c, length, direction):
            changes = place_word(grid, word, r, c, direction)
            used.add(word)
            if backtrack_fill(grid, remaining, words_by_len, used):
                return True
            used.remove(word)
            undo_changes(grid, changes)
    return False


def generate_crossword(language: str = "pl") -> List[List[str]]:
    pattern = random.choice(BLOCK_PATTERNS)
    grid = build_grid(pattern)
    across, down = find_slots(pattern)
    slots = [(r, c, l, 'A') for (r, c, l) in across] + [(r, c, l, 'D') for (r, c, l) in down]
    random.shuffle(slots)
    words = load_wordlist(language)
    words_by_len: Dict[int, List[str]] = {}
    for w in words:
        words_by_len.setdefault(len(w), []).append(w)
    used: set = set()
    success = backtrack_fill(grid, slots, words_by_len, used)
    if not success:
        # Retry a few times with different patterns
        for _ in range(5):
            pattern = random.choice(BLOCK_PATTERNS)
            grid = build_grid(pattern)
            across, down = find_slots(pattern)
            slots = [(r, c, l, 'A') for (r, c, l) in across] + [(r, c, l, 'D') for (r, c, l) in down]
            random.shuffle(slots)
            if backtrack_fill(grid, slots, words_by_len, set()):
                success = True
                break
    if not success:
        # Fallback: return the empty grid pattern (no prefilled letters)
        return grid
    return grid


def render_crossword_pdf(grid: List[List[str]], filename: str, trim_size: str = "8.5x11"):
    from reportlab.lib.colors import black, lightgrey, white
    from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    grid_size = min(page_width, page_height) - 2 * margin
    cell_size = grid_size / GRID_SIZE
    origin_x = (page_width - grid_size) / 2
    origin_y = (page_height - grid_size) / 2

    canvas.setLineWidth(1)

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
    canvas.save()