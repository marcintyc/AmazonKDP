import random
from typing import List, Tuple

from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number, DEFAULT_MARGIN, draw_page_title


def render_multiplication_table_pdf(filename: str, upto: int = 10, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    draw_page_title(canvas, page_width, page_height, f"Multiplication Table up to {upto}")

    # compute grid area below title
    top_space = 40
    grid_w = page_width - 2 * margin
    grid_h = page_height - 2 * margin - top_space
    cell = min(grid_w / (upto + 1), grid_h / (upto + 1))

    total_w = cell * (upto + 1)
    total_h = cell * (upto + 1)
    x0 = (page_width - total_w) / 2
    y0 = (page_height - total_h) / 2 - 10

    # draw grid with thicker header lines
    for r in range(upto + 2):
        y = y0 + r * cell
        lw = 2 if r in (1, upto + 1) else 1
        canvas.setLineWidth(lw)
        canvas.line(x0, y, x0 + total_w, y)
    for c in range(upto + 2):
        x = x0 + c * cell
        lw = 2 if c in (1, upto + 1) else 1
        canvas.setLineWidth(lw)
        canvas.line(x, y0, x, y0 + total_h)

    # header row/col and cells
    canvas.setFont("Helvetica", 11)
    for r in range(upto + 1):
        for c in range(upto + 1):
            x = x0 + c * cell
            y = y0 + (upto - r) * cell
            # skip top-left corner (header corner)
            if r == upto and c == 0:
                continue
            if r == upto:
                # header top row numbers (1..upto)
                val = c
            elif c == 0:
                # header left col numbers (1..upto)
                val = upto - r
            else:
                rr = upto - r
                cc = c
                text = f"{rr}×{cc}=____"
                cx = x + cell / 2
                cy = y + cell / 2 - 5
                canvas.drawCentredString(cx, cy, text)
                continue
            # center header numbers
            cx = x + cell / 2
            cy = y + cell / 2 - 5
            if val != 0:
                canvas.setFont("Helvetica-Bold", 12)
                canvas.drawCentredString(cx, cy, str(val))
                canvas.setFont("Helvetica", 11)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_simple_arithmetic_pdf(filename: str, problems: int = 50, max_num: int = 20, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    draw_page_title(canvas, page_width, page_height, "Simple Arithmetic")

    cols = 2
    col_w = (page_width - 2 * margin) / cols
    x_positions = [margin, margin + col_w]
    y = page_height - margin - 40
    row_h = 28
    page_num = 1

    ops = ['+', '-', '×']
    for i in range(1, problems + 1):
        a = random.randint(0, max_num)
        b = random.randint(0, max_num)
        op = random.choice(ops)
        if op == '-' and b > a:
            a, b = b, a
        text = f"{i:02d}.  {a} {op} {b} = __________________"
        col = 0 if (i - 1) % cols == 0 else 1
        x = x_positions[col]
        canvas.setFont("Helvetica", 13)
        canvas.drawString(x, y, text)
        if col == 1:
            y -= row_h
        if y < margin + 40:
            draw_footer_page_number(canvas, page_width, margin, page_num)
            canvas.showPage()
            draw_page_title(canvas, page_width, page_height, "Simple Arithmetic")
            y = page_height - margin - 40
            page_num += 1

    draw_footer_page_number(canvas, page_width, margin, page_num)
    canvas.showPage()
    canvas.save()


def _place_word_search(grid: List[List[str]], word: str) -> bool:
    n = len(grid)
    dirs = [(1,0), (0,1), (1,1), (1,-1), (-1,0), (0,-1), (-1,-1), (-1,1)]
    random.shuffle(dirs)
    positions = [(r, c) for r in range(n) for c in range(n)]
    random.shuffle(positions)
    for r, c in positions:
        for dr, dc in dirs:
            r2 = r + dr * (len(word) - 1)
            c2 = c + dc * (len(word) - 1)
            if not (0 <= r2 < n and 0 <= c2 < n):
                continue
            ok = True
            for i, ch in enumerate(word):
                rr = r + dr * i
                cc = c + dc * i
                if grid[rr][cc] not in ('.', ch):
                    ok = False
                    break
            if ok:
                for i, ch in enumerate(word):
                    rr = r + dr * i
                    cc = c + dc * i
                    grid[rr][cc] = ch
                return True
    return False


def render_word_search_pdf(filename: str, words: List[str], size: int = 12, trim_size: str = "8.5x11"):
    from reportlab.lib.colors import black
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    draw_page_title(canvas, page_width, page_height, "Word Search")

    grid = [['.' for _ in range(size)] for _ in range(size)]
    placed = []
    for w in words:
        w = w.upper()
        if 3 <= len(w) <= size and _place_word_search(grid, w):
            placed.append(w)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '.':
                grid[r][c] = random.choice(alphabet)

    grid_size = min(page_width, page_height) - 2 * margin
    cell = grid_size / size
    x0 = (page_width - grid_size) / 2
    y0 = (page_height - grid_size) / 2

    canvas.setFont("Helvetica", 12)
    for r in range(size):
        for c in range(size):
            x = x0 + c * cell
            y = y0 + (size - 1 - r) * cell
            canvas.rect(x, y, cell, cell, stroke=1, fill=0)
            ch = grid[r][c]
            canvas.drawCentredString(x + cell / 2, y + cell * 0.35, ch)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()

    if placed:
        draw_page_title(canvas, page_width, page_height, "Word List")
        canvas.setFont("Helvetica", 12)
        col_w = (page_width - 2 * margin) / 3
        x = margin
        y = page_height - margin - 50
        line_h = 16
        col = 0
        for w in sorted(placed):
            canvas.drawString(x + col * col_w, y, w)
            y -= line_h
            if y < margin + 20:
                col += 1
                y = page_height - margin - 50
                if col > 2:
                    canvas.showPage()
                    canvas.setFont("Helvetica", 12)
                    col = 0

    draw_footer_page_number(canvas, page_width, margin, 2)
    canvas.showPage()
    canvas.save()


def render_maze_pdf(filename: str, size: int = 15, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    n = size
    grid = [[0] * n for _ in range(n)]  # 0 wall, 1 path

    def carve(r: int, c: int):
        grid[r][c] = 1
        dirs = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            r2 = r + dr * 2
            c2 = c + dc * 2
            if 0 <= r2 < n and 0 <= c2 < n and grid[r2][c2] == 0:
                grid[r + dr][c + dc] = 1
                grid[r2][c2] = 1
                carve(r2, c2)

    carve(0, 0)

    draw_page_title(canvas, page_width, page_height, "Maze")

    grid_draw = min(page_width, page_height) - 2 * margin
    cell = grid_draw / n
    x0 = (page_width - grid_draw) / 2
    y0 = (page_height - grid_draw) / 2

    canvas.setLineWidth(2)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                x = x0 + c * cell
                y = y0 + (n - 1 - r) * cell
                canvas.rect(x, y, cell, cell, stroke=1, fill=1)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()