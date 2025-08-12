from flask import Flask, request, send_file, render_template_string
import os
from kdp_generator.cli import SUPPORTED_TRIM_SIZES
from kdp_generator.crossword import generate_crossword, render_crossword_pdf
from kdp_generator.sudoku import make_puzzle, render_sudoku_pdf
from kdp_generator.coloring import render_coloring_pdf
from kdp_generator.notebook import render_notebook_pdf

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>KDP Low-Content Generator</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.5; }
    h1 { margin-bottom: 0.5rem; }
    form { border: 1px solid #ddd; padding: 1rem; margin-bottom: 1.5rem; border-radius: 8px; }
    label { display: block; margin: 0.25rem 0; font-weight: 600; }
    input, select { padding: 0.4rem; margin: 0.25rem 0 0.75rem; width: 100%; max-width: 420px; }
    button { padding: 0.5rem 0.9rem; border: none; background: #0d6efd; color: white; border-radius: 6px; cursor: pointer; }
    button:hover { background: #0b5ed7; }
  </style>
</head>
<body>
  <h1>KDP Low-Content Generator</h1>
  <p>Generate printable PDFs for crosswords, sudoku, coloring pages, and notebooks.</p>

  <form method="post" action="/crossword">
    <h3>Crossword 10x10</h3>
    <label>Language</label>
    <select name="lang">
      <option value="pl">Polish</option>
      <option value="en">English</option>
    </select>
    <label>Trim size</label>
    <select name="trim">
      {% for s in sizes %}<option value="{{s}}">{{s}}</option>{% endfor %}
    </select>
    <button type="submit">Generate PDF</button>
  </form>

  <form method="post" action="/sudoku">
    <h3>Sudoku</h3>
    <label>Difficulty</label>
    <select name="difficulty">
      <option value="easy">Easy</option>
      <option value="medium">Medium</option>
    </select>
    <label>Pages</label>
    <input name="pages" type="number" value="5" min="1" max="50" />
    <label>Trim size</label>
    <select name="trim">
      {% for s in sizes %}<option value="{{s}}">{{s}}</option>{% endfor %}
    </select>
    <button type="submit">Generate PDF</button>
  </form>

  <form method="post" action="/coloring">
    <h3>Coloring Pages</h3>
    <label>Kind</label>
    <select name="kind">
      <option value="geometric">Geometric</option>
      <option value="mandala">Mandala</option>
    </select>
    <label>Pages</label>
    <input name="pages" type="number" value="20" min="1" max="100" />
    <label>Trim size</label>
    <select name="trim">
      {% for s in sizes %}<option value="{{s}}">{{s}}</option>{% endfor %}
    </select>
    <button type="submit">Generate PDF</button>
  </form>

  <form method="post" action="/notebook">
    <h3>Notebook / Journal</h3>
    <label>Title</label>
    <input name="title" type="text" value="My Awesome Journal" />
    <label>Style</label>
    <select name="style">
      <option value="lined">Lined</option>
      <option value="dotted">Dotted</option>
      <option value="blank">Blank</option>
    </select>
    <label>Pages</label>
    <input name="pages" type="number" value="120" min="1" max="300" />
    <label>Trim size</label>
    <select name="trim">
      {% for s in sizes %}<option value="{{s}}">{{s}}</option>{% endfor %}
    </select>
    <button type="submit">Generate PDF</button>
  </form>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(TEMPLATE, sizes=SUPPORTED_TRIM_SIZES)


@app.post("/crossword")
def make_crossword():
    lang = request.form.get("lang", "pl")
    trim = request.form.get("trim", "8.5x11")
    out = os.path.abspath("samples/crossword_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    grid = generate_crossword(language=lang)
    render_crossword_pdf(grid, out, trim)
    return send_file(out, as_attachment=True)


@app.post("/sudoku")
def make_sudoku():
    difficulty = request.form.get("difficulty", "easy")
    pages = int(request.form.get("pages", 5))
    trim = request.form.get("trim", "8.5x11")
    out = os.path.abspath("samples/sudoku_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    puzzles = [make_puzzle(difficulty=difficulty) for _ in range(pages)]
    render_sudoku_pdf(puzzles, out, trim)
    return send_file(out, as_attachment=True)


@app.post("/coloring")
def make_coloring():
    kind = request.form.get("kind", "geometric")
    pages = int(request.form.get("pages", 20))
    trim = request.form.get("trim", "8.5x11")
    out = os.path.abspath("samples/coloring_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render_coloring_pdf(kind, pages, out, trim)
    return send_file(out, as_attachment=True)


@app.post("/notebook")
def make_notebook():
    title = request.form.get("title", "My Journal")
    style = request.form.get("style", "lined")
    pages = int(request.form.get("pages", 120))
    trim = request.form.get("trim", "6x9")
    out = os.path.abspath("samples/notebook_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render_notebook_pdf(title, pages, style, out, trim)
    return send_file(out, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)