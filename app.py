from flask import Flask, request, send_file, render_template_string
import os
from kdp_generator.cli import SUPPORTED_TRIM_SIZES
from kdp_generator.crossword import generate_crossword, render_crossword_pdf
from kdp_generator.sudoku import make_puzzle, render_sudoku_pdf
from kdp_generator.coloring import render_coloring_pdf
from kdp_generator.notebook import render_notebook_pdf
from kdp_generator.worksheets import (
    render_multiplication_table_pdf,
    render_simple_arithmetic_pdf,
    render_word_search_pdf,
    render_maze_pdf,
)

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
      <option value="kids">Kids (thick, simple)</option>
      <option value="infant">Infant (high-contrast)</option>
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

  <form method="post" action="/multiplication">
    <h3>Multiplication Table</h3>
    <label>Up to</label>
    <input name="upto" type="number" value="10" min="5" max="20" />
    <label>Trim size</label>
    <select name="trim">
      {% for s in sizes %}<option value="{{s}}">{{s}}</option>{% endfor %}
    </select>
    <button type="submit">Generate PDF</button>
  </form>

  <form method="post" action="/arithmetic">
    <h3>Simple Arithmetic</h3>
    <label>Problems</label>
    <input name="problems" type="number" value="50" min="10" max="200" />
    <label>Max number</label>
    <input name="max" type="number" value="20" min="5" max="100" />
    <label>Trim size</label>
    <select name="trim">
      {% for s in sizes %}<option value="{{s}}">{{s}}</option>{% endfor %}
    </select>
    <button type="submit">Generate PDF</button>
  </form>

  <form method="post" action="/wordsearch">
    <h3>Word Search</h3>
    <label>Language</label>
    <select name="lang">
      <option value="en">English</option>
      <option value="pl">Polish</option>
    </select>
    <label>Size</label>
    <input name="size" type="number" value="12" min="8" max="20" />
    <label>Trim size</label>
    <select name="trim">
      {% for s in sizes %}<option value="{{s}}">{{s}}</option>{% endfor %}
    </select>
    <button type="submit">Generate PDF</button>
  </form>

  <form method="post" action="/maze">
    <h3>Maze</h3>
    <label>Size</label>
    <input name="size" type="number" value="15" min="7" max="31" />
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
    grid, words = generate_crossword(language=lang)
    render_crossword_pdf(grid, out, trim, words=words)
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


@app.post("/multiplication")
def make_multiplication():
    upto = int(request.form.get("upto", 10))
    trim = request.form.get("trim", "8.5x11")
    out = os.path.abspath("samples/multiplication_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render_multiplication_table_pdf(out, upto=upto, trim_size=trim)
    return send_file(out, as_attachment=True)


@app.post("/arithmetic")
def make_arithmetic():
    problems = int(request.form.get("problems", 50))
    max_num = int(request.form.get("max", 20))
    trim = request.form.get("trim", "8.5x11")
    out = os.path.abspath("samples/arithmetic_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render_simple_arithmetic_pdf(out, problems=problems, max_num=max_num, trim_size=trim)
    return send_file(out, as_attachment=True)


@app.post("/wordsearch")
def make_wordsearch():
    size = int(request.form.get("size", 12))
    lang = request.form.get("lang", "en")
    trim = request.form.get("trim", "8.5x11")
    out = os.path.abspath("samples/wordsearch_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    from kdp_generator.crossword import load_wordlist
    words = load_wordlist(lang)[:20]
    render_word_search_pdf(out, words=words, size=size, trim_size=trim)
    return send_file(out, as_attachment=True)


@app.post("/maze")
def make_maze():
    size = int(request.form.get("size", 15))
    trim = request.form.get("trim", "8.5x11")
    out = os.path.abspath("samples/maze_web.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render_maze_pdf(out, size=size, trim_size=trim)
    return send_file(out, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)