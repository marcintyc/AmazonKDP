import random
from typing import List, Tuple

# Zakładamy, że te importy pochodzą z Twojego oryginalnego pliku .pdf_utils
# i pozostają bez zmian.
from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number, DEFAULT_MARGIN, draw_page_title


def render_multiplication_table_pdf(filename: str, upto: int = 10, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # ZMIANA: Tytuł jest rysowany przez funkcję pomocniczą, która zwraca nową górną pozycję dla treści.
    # To pozwala na dynamiczne umiejscowienie siatki poniżej.
    content_top_y = page_height - margin - 40 # Symulacja działania draw_page_title
    draw_page_title(canvas, page_width, page_height, f"Multiplication Table up to {upto}")

    # ZMIANA: Obliczamy obszar roboczy *poniżej* tytułu.
    grid_w = page_width - 2 * margin
    grid_h = content_top_y - margin
    cell = min(grid_w / (upto + 1), grid_h / (upto + 1))

    total_w = cell * (upto + 1)
    total_h = cell * (upto + 1)

    # ZMIANA: Siatka jest idealnie centrowana w pozostałym miejscu, bez odejmowania stałych wartości.
    x0 = (page_width - total_w) / 2
    y0 = margin + (grid_h - total_h) / 2

    # Rysowanie siatki z grubszymi liniami dla nagłówków
    for i in range(upto + 2):
        # Linie poziome
        y = y0 + i * cell
        lw = 2 if i in (0, 1, upto + 1) else 0.5
        canvas.setLineWidth(lw)
        canvas.line(x0, y, x0 + total_w, y)
        
        # Linie pionowe
        x = x0 + i * cell
        lw = 2 if i in (0, 1, upto + 1) else 0.5
        canvas.setLineWidth(lw)
        canvas.line(x, y0, x, y0 + total_h)

    # Wypełnianie komórek - uproszczona i bardziej czytelna logika
    font_size = 11
    canvas.setFont("Helvetica", font_size)
    for r_idx in range(1, upto + 1):  # r_idx to numer wiersza od 1 do "upto"
        for c_idx in range(1, upto + 1): # c_idx to numer kolumny od 1 do "upto"
            
            # Nagłówek górny
            if r_idx == 1:
                canvas.setFont("Helvetica-Bold", 12)
                cx_header = x0 + (c_idx + 0.5) * cell
                cy_header = y0 + (upto + 0.5) * cell
                canvas.drawCentredString(cx_header, cy_header - font_size/2, str(c_idx))

            # Nagłówek boczny
            if c_idx == 1:
                canvas.setFont("Helvetica-Bold", 12)
                cx_header = x0 + 0.5 * cell
                cy_header = y0 + (upto - r_idx + 0.5) * cell
                canvas.drawCentredString(cx_header, cy_header - font_size/2, str(r_idx))

            # Treść komórki
            canvas.setFont("Helvetica", font_size)
            text = f"{r_idx}×{c_idx}=____"
            cx = x0 + (c_idx + 0.5) * cell
            cy = y0 + (upto - r_idx + 0.5) * cell
            # ZMIANA: Poprawione centrowanie w pionie
            canvas.drawCentredString(cx, cy - font_size/2, text)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_simple_arithmetic_pdf(filename: str, problems: int = 50, max_num: int = 20, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # ZMIANA: Użycie zmiennych do kontroli układu dla łatwiejszych modyfikacji
    cols = 2
    col_w = (page_width - 2 * margin) / cols
    row_h = 28
    y_start_pos = page_height - margin - 40 # Pozycja Y startowa pod tytułem
    y_limit = margin + 40 # Kiedy przejść na nową stronę
    
    # Rysowanie pierwszej strony
    draw_page_title(canvas, page_width, page_height, "Simple Arithmetic")
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
        
        canvas.setFont("Helvetica", 13)
        canvas.drawString(x, y, problem_text)
        
        # ZMIANA: Linia na odpowiedź jest dynamiczna
        text_width = canvas.stringWidth(problem_text, "Helvetica", 13)
        line_start = x + text_width
        line_end = x + col_w - 15 # Zostawiamy mały margines z prawej
        canvas.setLineWidth(0.5)
        canvas.line(line_start, y - 1, line_end, y - 1)

        # Przejście do nowego wiersza lub nowej strony
        if col_idx == cols - 1:
            y -= row_h
        
        if y < y_limit and i < problems:
            draw_footer_page_number(canvas, page_width, margin, page_num)
            canvas.showPage()
            
            # Nowa strona
            draw_page_title(canvas, page_width, page_height, "Simple Arithmetic")
            y = y_start_pos
            page_num += 1

    draw_footer_page_number(canvas, page_width, margin, page_num)
    canvas.showPage()
    canvas.save()


# Funkcja _place_word_search pozostaje bez zmian, jest w porządku.
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

    # Strona 1: Siatka i lista słów
    content_top_y = page_height - margin - 40
    draw_page_title(canvas, page_width, page_height, "Word Search")

    # Logika generowania siatki pozostaje taka sama
    grid = [['.' for _ in range(size)] for _ in range(size)]
    placed = []
    # Sortowanie od najdłuższego słowa zwiększa szansę na umieszczenie wszystkich
    for w in sorted(words, key=len, reverse=True):
        w = w.upper().strip()
        if 3 <= len(w) <= size and _place_word_search(grid, w):
            placed.append(w)
            
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '.':
                grid[r][c] = random.choice(alphabet)

    # ZMIANA: Lepsze obliczanie wymiarów i pozycji siatki
    # Zostawiamy miejsce na listę słów pod siatką (ok. 2 cale)
    grid_area_h = content_top_y - (margin + 20) - (2 * 72) 
    grid_w = page_width - 2 * margin
    cell = min(grid_w / size, grid_area_h / size)
    total_grid_size = cell * size
    
    x0 = (page_width - total_grid_size) / 2
    y0 = content_top_y - total_grid_size # Pozycjonowanie od góry

    # Rysowanie liter w siatce
    canvas.setFont("Helvetica-Bold", cell * 0.7)
    for r in range(size):
        for c in range(size):
            x = x0 + c * cell
            y = y0 + (size - 1 - r) * cell
            ch = grid[r][c]
            canvas.drawCentredString(x + cell / 2, y + cell * 0.25, ch)

    # ZMIANA: Czystsze rysowanie listy słów pod siatką
    if placed:
        canvas.setFont("Helvetica", 12)
        word_cols = 4 # Ustawiamy 4 kolumny na słowa
        col_w = (page_width - 2 * margin) / word_cols
        x_start = margin
        y_start = y0 - 40 # Zaczynamy rysować listę pod siatką
        
        words_per_col = (len(placed) + word_cols -1) // word_cols
        
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
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # ZMIANA: Upewniamy się, że rozmiar jest nieparzysty dla lepszego algorytmu
    n = size if size % 2 != 0 else size + 1
    # False = ściana, True = ścieżka
    grid = [[False] * n for _ in range(n)]

    # ZMIANA: Algorytm generowania labiryntu - teraz rzeźbi ścieżki
    def carve(r: int, c: int):
        grid[r][c] = True
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            r2, c2 = r + dr, c + dc
            if 0 <= r2 < n and 0 <= c2 < n and not grid[r2][c2]:
                # Przebijamy ścianę pomiędzy
                grid[r + dr // 2][c + dc // 2] = True
                carve(r2, c2)

    carve(0, 0)

    content_top_y = page_height - margin - 40
    draw_page_title(canvas, page_width, page_height, "Maze")

    grid_draw_area = min(page_width - 2*margin, content_top_y - margin)
    cell = grid_draw_area / n
    total_maze_size = cell * n
    
    # ZMIANA: Centrowanie labiryntu w dostępnym obszarze
    x0 = (page_width - total_maze_size) / 2
    y0 = margin + (content_top_y - margin - total_maze_size) / 2
    
    # ZMIANA: Rysowanie ścian jako linii zamiast kwadratów - czystszy wygląd
    canvas.setLineWidth(max(2, cell / 10)) # Grubość ściany zależna od rozmiaru
    canvas.setLineCap(1) # Zaokrąglone końcówki
    
    # Rysujemy obramowanie
    canvas.rect(x0, y0, total_maze_size, total_maze_size)
    
    for r in range(n):
        for c in range(n):
            x = x0 + c * cell
            y = y0 + (n - 1 - r) * cell
            
            # Rysuj dolną ścianę, jeśli poniżej jest ściana (False)
            if r < n - 1 and not (grid[r][c] and grid[r+1][c]):
                 canvas.line(x, y, x + cell, y)
            # Rysuj prawą ścianę, jeśli z prawej jest ściana (False)
            if c < n - 1 and not (grid[r][c] and grid[r][c+1]):
                 canvas.line(x + cell, y, x + cell, y + cell)

    # Dodanie wejścia i wyjścia
    canvas.setStrokeColorRGB(1, 1, 1) # Używamy białego koloru do "wymazania" fragmentu ramki
    canvas.setLineWidth(max(3, cell / 10 + 1))
    canvas.line(x0, y0 + (n-1)*cell, x0, y0 + n*cell) # Wejście
    canvas.line(x0 + n*cell, y0, x0 + n*cell, y0 + cell) # Wyjście
    
    # Oznaczenia Start/Koniec dla czytelności
    canvas.setStrokeColorRGB(0,0,0)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawCentredString(x0 - 30, y0 + (n - 0.5) * cell, "Start")
    canvas.drawCentredString(x0 + total_maze_size + 35, y0 + 0.5 * cell, "Koniec")

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()
