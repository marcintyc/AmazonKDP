# Amazon KDP — Generator książek low-content

Projekt w Pythonie generujący automatycznie książki typu low-content gotowe do sprzedaży na Amazon KDP:
- Krzyżówki 10x10 (z bazą słów PL/EN)
- Sudoku (poziom łatwy/średni, unikalne rozwiązania)
- Kolorowanki (proste wzory geometryczne i mandale)
- Notatniki / journale (okładka z tytułem użytkownika, style: lined/dotted/blank)

PDF generowane są w popularnych wymiarach KDP: `6x9`, `8.5x11`, `8x10`, `7x10`.

## Szybki start (CLI)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Sudoku
python -m kdp_generator.cli sudoku --pages 5 --difficulty easy --trim 8.5x11 --out samples/sudoku.pdf

# Krzyżówka
python -m kdp_generator.cli crossword --lang pl --trim 8.5x11 --out samples/crossword.pdf

# Kolorowanki
python -m kdp_generator.cli coloring --kind mandala --pages 20 --trim 8.5x11 --out samples/coloring.pdf

# Notatnik
python -m kdp_generator.cli notebook --title "Mój dziennik" --style lined --pages 120 --trim 6x9 --out samples/notebook.pdf
```

## Interfejs web (lokalnie)

```bash
export FLASK_APP=app.py
flask run
```

Otwórz `http://localhost:5000` i użyj formularzy do generowania PDF.

## Struktura

- `kdp_generator/` — logika generatorów i narzędzia PDF
  - `crossword.py` — generator krzyżówek 10x10 (fill-in)
  - `sudoku.py` — generator sudoku z unikalnymi rozwiązaniami
  - `coloring.py` — wzory kolorowanek (geometria/mandale)
  - `notebook.py` — notatnik/journal z okładką i wnętrzem
  - `pdf_utils.py` — pomocnicze do rozmiarów KDP i rysowania
  - `wordlists/` — listy słów `polish.txt`, `english.txt`
- `kdp_generator/cli.py` — interfejs wiersza poleceń
- `app.py` — prosty serwer Flask
- `docs/` — GitHub Pages z instrukcją

## Uwaga dot. KDP

- Upewnij się, że rozmiar `trim` jest zgodny z formatem publikacji (np. `6x9` dla notatników, `8.5x11` dla kolorowanek).
- W razie potrzeby dodaj spady/bleed (obecnie brak; można rozszerzyć w `pdf_utils.py`).
- Krzyżówki: prosta wypełnianka ze stałą siatką 10x10.

## Licencja

MIT