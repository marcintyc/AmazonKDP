import random
from typing import List, Tuple
from reportlab.lib.colors import black

# Zakładamy, że importy z pdf_utils są poprawne
from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number, DEFAULT_MARGIN, draw_page_title


def render_multiplication_table_pdf(filename: str, upto: int = 10, trim_size: str = "8.5x11"):
    # Walidacja parametrów
    if upto < 1 or upto > 20:  # Ograniczenie, aby uniknąć zbyt dużych siatek
        raise ValueError("Parameter 'upto' must be between 1 and 20.")

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # Tytuł i pozycja treści
    content_top_y = draw_page_title(canvas, page_width, page_height, f"Multiplication Table up to {upto}")

    # Obliczanie siatki
    grid_w = page_width - 2 * margin
    grid_h = content_top_y - margin - 40  # Dodatkowy odstęp na dole
    cell = min(grid_w / (upto + 1), grid_h / (upto + 1))
    total_w = cell * (upto + 1)
    total_h = cell * (upto + 1)

    # Centrowanie siatki
    x0 = (page_width - total_w) / 2
    y0 = margin + (content_top_y - margin - total_h) / 2

    # Rysowanie siatki
    canvas.setStrokeColor(black)
    for i in range(upto + 2):
        # Linie poziome
        y = y0 + i * cell
        canvas.setLineWidth(2 if i in (0, 1, upto + 1) else 0.5)
        canvas.line(x0, y, x0 + total_w, y)

        # Linie pionowe
        x = x0 + i * cell
        canvas.setLineWidth(2 if i in (0, 1, upto + 1) else 0.5)
        canvas.line(x, y0, x, y0 + total_h)

    # Wypełnianie komórek
    font_size = min(12, cell * 0.5)  # Dynamiczna wielkość czcionki
    canvas.setFont("Helvetica", font_size)
    for r_idx in range(1, upto + 1):
        for c_idx in range(1, upto + 1):
            # Nagłówki
            if r_idx == 1:
                canvas.setFont("Helvetica-Bold", font_size + 2)
                cx_header = x0 + (c_idx + 0.5) * cell
                cy_header = y0 + (upto + 0.5) * cell
                canvas.drawCentredString(cx_header, cy_header - font_size / 2, str(c_idx))

            if c_idx == 1:
                canvas.setFont("Helvetica-Bold", font_size + 2)
                cx_header = x0 + 0.5 * cell
                cy_header = y0 + (upto - r_idx + 0.5) * cell
                canvas.drawCentredString(cx_header, cy_header - font_size / 2, str(r_idx))

            # Treść komórki
            canvas.setFont("Helvetica", font_size)
            text = f"{r_idx} × {c_idx} = ____"
            cx = x0 + (c_idx + 0.5) * cell
            cy = y0 + (upto - r_idx + 0.5) * cell
            canvas.drawCentredString(cx, cy - font_size / 2, text)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_simple_arithmetic_pdf(filename: str, problems: int = 50, max_num: int = 20, trim_size: str = "8.5x11"):
    # Walidacja parametrów
    if problems < 1 or problems > 100:
        raise ValueError("Parameter 'problems' must be between 1 and 100.")
    if max_num < 1 or max_num > 100:
        raise ValueError("Parameter 'max_num' must be between 1 and 100.")

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # Układ
    cols = 2
    col_w = (page_width - 2 * margin) / cols
    row_h = 28
    y_start_pos = draw_page_title(canvas, page_width, page_height, "Simple Arithmetic")
    y_limit = margin + 40
    y = y_start_pos
    page_num = 1

    ops = ['+', '-', '×']
    for i in range(1, problems + 1):
        a = random.randint(0, max_num)
        b = random.randint(0, max_num)
        op = random.choice(ops)
        if op == '-' and b > a:
            a, b = b, a

        problem_text = f"{i:02d}.  {a} {op} {b} = "

        col_idx = (i - 1) % cols
        x = margin + col_idx * col_w

        # Rysowanie zadania
        canvas.setFont("Helvetica", 14)  # Większa czcionka dla czytelności
        canvas.drawString(x, y, problem_text)

        # Linia odpowiedzi
        text_width = canvas.stringWidth(problem_text, "Helvetica", 14)
        line_start = x + text_width + 5
        line_end = x + col_w - 10
        canvas.setLineWidth(0.5)
        canvas.line(line_start, y - 2, line_end, y - 2)

        # Przejście do nowego wiersza lub strony
        if col_idx == cols - 1:
            y -= row_h

        if y < y_limit and i < problems:
            draw_footer_page_number(canvas, page_width, margin, page_num)
            canvas.showPage()
            draw_page_title(canvas, page_width, page_height, "Simple Arithmetic")
            y = y_start_pos
            page_num += 1

    draw_footer_page_number(canvas, page_width, margin, page_num)
    canvas.showPage()
    canvas.save()


def render_word_search_pdf(filename: str, words: List[str], size: int = 12, trim_size: str = "8.5x11"):
    # Walidacja parametrów
    if size < 5 or size > 20:
        raise ValueError("Parameter 'size' must be between 5 and 20.")
    if not words:
        raise ValueError("List of words cannot be empty.")

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # Strona 1: Siatka i lista słów
    content_top_y = draw_page_title(canvas, page_width, page_height, "Word Search")

    # Generowanie siatki
    grid = [['.' for _ in range(size)] for _ in range(size)]
    placed = []
    for w in sorted(words, key=len, reverse=True):
        w = w.upper().strip()
        if 3 <= len(w) <= size and _place_word_search(grid, w):
            placed.append(w)

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '.':
                grid[r][c] = random.choice(alphabet)

    # Obliczanie wymiarów siatki
    grid_area_h = content_top_y - margin - 2 * 72  # Miejsce na listę słów
    grid_w = page_width - 2 * margin
    cell = min(grid_w / size, grid_area_h / size)
    total_grid_size = cell * size

    x0 = (page_width - total_grid_size) / 2
    y0 = content_top_y - total_grid_size

    # Rysowanie liter
    font_size = min(14, cell * 0.7)
    canvas.setFont("Helvetica-Bold", font_size)
    for r in range(size):
        for c in range(size):
            x = x0 + c * cell
            y = y0 + (size - 1 - r) * cell
            canvas.drawCentredString(x + cell / 2, y + cell * 0.25, grid[r][c])

    # Lista słów
    if placed:
        canvas.setFont("Helvetica", 12)
        word_cols = 4
        col_w = (page_width - 2 * margin) / word_cols
        x_start = margin
        y_start = y0 - 50

        words_per_col = (len(placed) + word_cols - 1) // word_cols
        for i, word in enumerate(sorted(placed)):
            col_idx = i // words_per_col
            row_idx = i % words_per_col
            x = x_start + col_idx * col_w
            y = y_start - row_idx * 16
            canvas.drawString(x, y, word)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_maze_pdf(filename: str, size: int = 15, trim_size: str = "8.5x11"):
    # Walidacja parametrów
    if size < 5 or size > 30:
        raise ValueError("Parameter 'size' must be between 5 and 30.")

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # Generowanie labiryntu
    n = size if size % 2 != 0 else size + 1
    grid = [[False] * n for _ in range(n)]

    def carve(r: int, c: int):
        grid[r][c] = True
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            r2, c2 = r + dr, c + dc
            if 0 <= r2 < n and 0 <= c2 < n and not grid[r2][c2]:
                grid[r + dr // 2][c + dc // 2] = True
                carve(r2, c2)

    carve(0, 0)

    # Układ labiryntu
    content_top_y = draw_page_title(canvas, page_width, page_height, "Maze")
    grid_draw_area = min(page_width - 2 * margin, content_top_y - margin)
    cell = grid_draw_area / n
    total_maze_size = cell * n

    x0 = (page_width - total_maze_size) / 2
    y0 = margin + (content_top_y - margin - total_maze_size) / 2

    # Rysowanie labiryntu
    canvas.setLineWidth(max(2, cell / 10))
    canvas.setLineCap(1)
    canvas.rect(x0, y0, total_maze_size, total_maze_size)

    for r in range(n):
        for c in range(n):
            x = x0 + c * cell
            y = y0 + (n - 1 - r) * cell
            if r < n - 1 and not (grid[r][c] and grid[r + 1][c]):
                canvas.line(x, y, x + cell, y)
            if c < n - 1 and not (grid[r][c] and grid[r][c + 1]):
                canvas.line(x + cell, y, x + cell, y + cell)

    # Wejście i wyjście
    canvas.setStrokeColorRGB(1, 1, 1)
    canvas.setLineWidth(max(3, cell / 10 + 1))
    canvas.line(x0, y0 + (n - 1) * cell, x0, y0 + n * cell)
    canvas.line(x0 + n * cell, y0, x0 + n * cell, y0 + cell)

    # Oznaczenia
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawCentredString(x0 - 30, y0 + (n - 0.5) * cell, "Start")
    canvas.drawCentredString(x0 + total_maze_size + 35, y0 + 0.5 * cell, "Koniec")

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()
