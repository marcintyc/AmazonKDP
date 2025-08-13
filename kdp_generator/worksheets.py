# worksheet_generator.py
import random
from typing import List

# Importujemy nasze funkcje pomocnicze
from pdf_utils import (
    create_canvas, size_to_points, draw_footer_page_number, draw_page_title,
    DEFAULT_MARGIN, FONT_NAME, FONT_NAME_BOLD
)

def render_multiplication_table_pdf(filename: str, upto: int = 10, trim_size: str = "8.5x11"):
    """Generuje PDF z tabliczką mnożenia do wypełnienia."""
    c = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)

    content_top_y = draw_page_title(c, page_width, page_height, f"Tabliczka mnożenia do {upto}")

    # Definiujemy obszar roboczy dla siatki
    grid_area_w = page_width - 2 * DEFAULT_MARGIN
    grid_area_h = content_top_y - DEFAULT_MARGIN
    
    # Obliczamy rozmiar komórki, aby siatka się zmieściła
    cell_size = min(grid_area_w / (upto + 1), grid_area_h / (upto + 1))
    
    total_w = cell_size * (upto + 1)
    total_h = cell_size * (upto + 1)

    # Centrujemy siatkę w dostępnym obszarze roboczym
    x0 = (page_width - total_w) / 2
    y0 = DEFAULT_MARGIN + (grid_area_h - total_h) / 2

    # Rysowanie siatki
    for i in range(upto + 2):
        # Linie poziome
        y = y0 + i * cell_size
        lw = 2 if i in (0, 1, upto + 1) else 0.5
        c.setLineWidth(lw)
        c.line(x0, y, x0 + total_w, y)
        
        # Linie pionowe
        x = x0 + i * cell_size
        lw = 2 if i in (0, 1, upto + 1) else 0.5
        c.setLineWidth(lw)
        c.line(x, y0, x, y0 + total_h)
        
    # Wypełnianie siatki liczbami i polami
    for row in range(1, upto + 1):
        for col in range(1, upto + 1):
            # Nagłówki
            if row == 1:
                c.setFont(FONT_NAME_BOLD, 12)
                cx = x0 + (col + 0.5) * cell_size
                cy = y0 + (upto + 1 - 0.5) * cell_size
                c.drawCentredString(cx, cy - 4, str(col))
            if col == 1:
                c.setFont(FONT_NAME_BOLD, 12)
                cx = x0 + 0.5 * cell_size
                cy = y0 + (upto + 1 - row - 0.5) * cell_size
                c.drawCentredString(cx, cy - 4, str(row))
            
            # Pola do wypełnienia
            c.setFont(FONT_NAME, 11)
            text = f"{row} × {col} = ___"
            cx = x0 + (col + 0.5) * cell_size
            cy = y0 + (upto + 1 - row - 0.5) * cell_size
            c.drawCentredString(cx, cy - 4, text)

    draw_footer_page_number(c, page_width, 1)
    c.showPage()
    c.save()


def render_simple_arithmetic_pdf(filename: str, problems: int = 50, max_num: int = 20, trim_size: str = "8.5x11"):
    """Generuje PDF z prostymi zadaniami arytmetycznymi."""
    c = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    
    ops = ['+', '-', '×']
    cols = 2
    col_width = (page_width - 2 * DEFAULT_MARGIN) / cols
    row_height = 28
    page_num = 1
    
    def new_page():
        nonlocal y_pos
        if page_num > 1:
            draw_footer_page_number(c, page_width, page_num - 1)
            c.showPage()
        content_top_y = draw_page_title(c, page_width, page_height, "Prosta Arytmetyka")
        y_pos = content_top_y

    y_pos = 0
    new_page()

    for i in range(1, problems + 1):
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        op = random.choice(ops)
        
        if op == '-' and b > a: a, b = b, a
        if op == '×':
            a = random.randint(1, 10)
            b = random.randint(1, 10)

        problem_text = f"{i:2d}.   {a} {op} {b} = "
        
        # Sprawdzamy, czy potrzebna jest nowa strona
        if y_pos < DEFAULT_MARGIN + row_height:
            page_num += 1
            new_page()

        col_index = (i - 1) % cols
        x_pos = DEFAULT_MARGIN + col_index * col_width
        
        c.setFont(FONT_NAME, 13)
        c.drawString(x_pos, y_pos, problem_text)
        
        # Dynamiczna linia na odpowiedź
        text_width = c.stringWidth(problem_text, FONT_NAME, 13)
        line_start = x_pos + text_width
        line_end = x_pos + col_width - 20 # Zostawiamy trochę marginesu
        c.setLineWidth(0.5)
        c.line(line_start, y_pos - 1, line_end, y_pos - 1)

        if col_index == cols - 1:
            y_pos -= row_height

    draw_footer_page_number(c, page_width, page_num)
    c.showPage()
    c.save()


def _place_word_search(grid: List[List[str]], word: str) -> bool:
    """Pomocnicza funkcja do umieszczania słów w siatce."""
    n = len(grid)
    dirs = [(1,0), (0,1), (1,1), (1,-1), (-1,0), (0,-1), (-1,-1), (-1,1)]
    random.shuffle(dirs)
    positions = [(r, c) for r in range(n) for c in range(n)]
    random.shuffle(positions)
    for r_start, c_start in positions:
        for dr, dc in dirs:
            r_end = r_start + dr * (len(word) - 1)
            c_end = c_start + dc * (len(word) - 1)
            if not (0 <= r_end < n and 0 <= c_end < n):
                continue
            
            can_place = True
            for i in range(len(word)):
                r, c = r_start + dr * i, c_start + dc * i
                if grid[r][c] not in ('.', word[i]):
                    can_place = False
                    break
            
            if can_place:
                for i in range(len(word)):
                    r, c = r_start + dr * i, c_start + dc * i
                    grid[r][c] = word[i]
                return True
    return False

def render_word_search_pdf(filename: str, words: List[str], size: int = 15, trim_size: str = "8.5x11"):
    """Generuje PDF z wyszukiwanką słów."""
    c = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)

    # --- Strona 1: Siatka ---
    content_top_y = draw_page_title(c, page_width, page_height, "Wyszukiwanka Słowna")
    
    grid = [['.' for _ in range(size)] for _ in range(size)]
    placed_words = []
    for word in sorted(words, key=len, reverse=True):
        w_upper = word.upper().strip()
        if 3 <= len(w_upper) <= size and _place_word_search(grid, w_upper):
            placed_words.append(w_upper)
            
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for r in range(size):
        for c_idx in range(size):
            if grid[r][c_idx] == '.':
                grid[r][c_idx] = random.choice(alphabet)

    grid_area_w = page_width - 2 * DEFAULT_MARGIN
    grid_area_h = content_top_y - DEFAULT_MARGIN - (0.5*inch) # miejsce na listę słów pod spodem
    
    cell_size = min(grid_area_w / size, grid_area_h / size)
    total_grid_size = cell_size * size
    
    x0 = (page_width - total_grid_size) / 2
    y0 = content_top_y - total_grid_size

    c.setFont(FONT_NAME_BOLD, cell_size * 0.6)
    for r in range(size):
        for c_idx in range(size):
            x = x0 + c_idx * cell_size
            y = y0 + (size - 1 - r) * cell_size
            # Lepsze wizualnie jest rysowanie samych liter bez siatki
            # c.rect(x, y, cell_size, cell_size) 
            char = grid[r][c_idx]
            c.drawCentredString(x + cell_size / 2, y + cell_size * 0.25, char)

    # --- Lista słów pod siatką ---
    c.setFont(FONT_NAME, 11)
    word_cols = 4
    col_w = (page_width - 2 * DEFAULT_MARGIN) / word_cols
    x_start = DEFAULT_MARGIN
    y_start = y0 - (0.5 * inch)
    
    words_per_col = (len(placed_words) + word_cols -1) // word_cols
    
    for i, word in enumerate(sorted(placed_words)):
        col_idx = i // words_per_col
        row_idx = i % words_per_col
        x = x_start + col_idx * col_w
        y = y_start - row_idx * 15
        c.drawString(x, y, word)

    draw_footer_page_number(c, page_width, 1)
    c.showPage()
    c.save()


def render_maze_pdf(filename: str, size: int = 25, trim_size: str = "8.5x11"):
    """Generuje PDF z labiryntem."""
    c = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)

    content_top_y = draw_page_title(c, page_width, page_height, "Labirynt")

    # Upewnijmy się, że rozmiar jest nieparzysty dla lepszego generowania
    n = size if size % 2 != 0 else size + 1
    grid = [[False] * n for _ in range(n)] # False = ściana, True = ścieżka

    def carve(r, c_idx):
        grid[r][c_idx] = True
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            r2, c2 = r + dr, c_idx + dc
            if 0 <= r2 < n and 0 <= c2 < n and not grid[r2][c2]:
                grid[r + dr // 2][c_idx + dc // 2] = True
                carve(r2, c2)

    carve(0, 0) # Zaczynamy od lewego górnego rogu

    grid_area_w = page_width - 2 * DEFAULT_MARGIN
    grid_area_h = content_top_y - DEFAULT_MARGIN
    cell_size = min(grid_area_w / n, grid_area_h / n)
    total_size = cell_size * n
    
    x0 = (page_width - total_size) / 2
    y0 = DEFAULT_MARGIN + (grid_area_h - total_size) / 2
    
    # Rysujemy ściany jako linie, co wygląda znacznie lepiej
    c.setLineWidth(2)
    c.setLineCap(1) # Zaokrąglone końcówki linii
    for r in range(n):
        for c_idx in range(n):
            if not grid[r][c_idx]: continue # Rysujemy tylko ściany dla ścieżek
            
            x = x0 + c_idx * cell_size
            y = y0 + (n - 1 - r) * cell_size
            
            # Ściana górna?
            if r > 0 and not grid[r - 1][c_idx]:
                c.line(x, y + cell_size, x + cell_size, y + cell_size)
            # Ściana lewa?
            if c_idx > 0 and not grid[r][c_idx - 1]:
                c.line(x, y, x, y + cell_size)

    # Rysujemy ramkę zewnętrzną i wejście/wyjście
    c.rect(x0, y0, total_size, total_size)
    c.setStrokeColorRGB(1, 1, 1) # Biały kolor do "wymazania" wejścia
    c.line(x0, y0 + (n-1) * cell_size, x0, y0 + n * cell_size)
    c.line(x0 + n * cell_size, y0, x0 + n * cell_size, y0 + cell_size)
    
    # Oznaczenia Start/Koniec
    c.setStrokeColorRGB(0, 0, 0)
    c.setFont(FONT_NAME_BOLD, 12)
    c.drawCentredString(x0 - 30, y0 + (n - 0.5) * cell_size, "Start")
    c.drawCentredString(x0 + total_size + 30, y0 + 0.5 * cell_size, "Koniec")
    
    draw_footer_page_number(c, page_width, 1)
    c.showPage()
    c.save()


if __name__ == '__main__':
    print("Generowanie arkuszy PDF...")
    render_multiplication_table_pdf("multiplication_table.pdf", upto=12)
    render_simple_arithmetic_pdf("simple_arithmetic.pdf", problems=60, max_num=25)
    
    word_list = ["PYTHON", "REPORTLAB", "GEMINI", "KODOWANIE", "ZABAWA", "NAUKA", "ALGORYTM"]
    render_word_search_pdf("word_search.pdf", words=word_list, size=15)
    
    render_maze_pdf("maze.pdf", size=31)
    print("Gotowe!")
