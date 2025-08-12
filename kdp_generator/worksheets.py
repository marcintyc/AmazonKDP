import random
from typing import List, Tuple


def render_multiplication_table_pdf(filename: str, upto: int = 10, trim_size: str = "8.5x11"):
    from reportlab.lib.colors import black
    from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    cell = min((page_width - 2 * margin) / (upto + 1), (page_height - 2 * margin) / (upto + 1))
    x0 = (page_width - cell * (upto + 1)) / 2
    y0 = (page_height - cell * (upto + 1)) / 2

    canvas.setFont("Helvetica", 12)

    for r in range(upto + 1):
        for c in range(upto + 1):
            x = x0 + c * cell
            y = y0 + (upto - r) * cell
            canvas.rect(x, y, cell, cell, stroke=1, fill=0)
            if r == 0 and c == 0:
                continue
            if r == 0:
                canvas.drawCentredString(x + cell / 2, y + cell / 2 - 4, str(c))
            elif c == 0:
                canvas.drawCentredString(x + cell / 2, y + cell / 2 - 4, str(r))
            else:
                text = f"{r}×{c}=____"
                canvas.drawCentredString(x + cell / 2, y + cell / 2 - 4, text)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_simple_arithmetic_pdf(filename: str, problems: int = 50, max_num: int = 20, trim_size: str = "8.5x11"):
    from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    canvas.setFont("Helvetica", 14)
    x = margin
    y = page_height - margin
    col_w = (page_width - 2 * margin) / 3
    row_h = 24
    page_num = 1

    ops = ['+', '-', '×']
    for i in range(1, problems + 1):
        a = random.randint(0, max_num)
        b = random.randint(0, max_num)
        op = random.choice(ops)
        if op == '-' and b > a:
            a, b = b, a
        text = f"{i:02d}.  {a} {op} {b} = _______"
        canvas.drawString(x, y, text)
        y -= row_h
        if y < margin + row_h:
            draw_footer_page_number(canvas, page_width, margin, page_num)
            canvas.showPage()
            canvas.setFont("Helvetica", 14)
            y = page_height - margin
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
    from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

    # build grid
    grid = [['.' for _ in range(size)] for _ in range(size)]
    placed = []
    for w in words:
        w = w.upper()
        if 3 <= len(w) <= size and _place_word_search(grid, w):
            placed.append(w)
    # fill remaining
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '.':
                grid[r][c] = random.choice(alphabet)

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

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
            tw = canvas.stringWidth(ch, "Helvetica", 12)
            canvas.drawString(x + (cell - tw) / 2, y + cell * 0.3, ch)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()

    if placed:
        canvas.setFont("Helvetica-Bold", 18)
        title = "Word List"
        tw = canvas.stringWidth(title, "Helvetica-Bold", 18)
        canvas.drawString((page_width - tw) / 2, page_height - margin - 20, title)
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
    # Simple DFS backtracker maze
    from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

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

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    grid_size = min(page_width, page_height) - 2 * margin
    cell = grid_size / n
    x0 = (page_width - grid_size) / 2
    y0 = (page_height - grid_size) / 2

    # draw maze walls
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