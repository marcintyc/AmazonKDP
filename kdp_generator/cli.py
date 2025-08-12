import argparse
import os
from typing import List

from .crossword import generate_crossword, render_crossword_pdf
from .sudoku import make_puzzle, render_sudoku_pdf
from .coloring import render_coloring_pdf
from .notebook import render_notebook_pdf
from .worksheets import (
    render_multiplication_table_pdf,
    render_simple_arithmetic_pdf,
    render_word_search_pdf,
    render_maze_pdf,
)


SUPPORTED_TRIM_SIZES = ["6x9", "8.5x11", "8x10", "7x10"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="KDP Low-Content Book Generator")
    sub = parser.add_subparsers(dest="command", required=True)

    # Crossword
    p1 = sub.add_parser("crossword", help="Generate a 10x10 crossword")
    p1.add_argument("--lang", choices=["pl", "en"], default="pl")
    p1.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p1.add_argument("--out", default="samples/crossword.pdf")

    # Sudoku
    p2 = sub.add_parser("sudoku", help="Generate Sudoku pages")
    p2.add_argument("--difficulty", choices=["easy", "medium"], default="easy")
    p2.add_argument("--pages", type=int, default=5)
    p2.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p2.add_argument("--out", default="samples/sudoku.pdf")

    # Coloring
    p3 = sub.add_parser("coloring", help="Generate coloring pages")
    p3.add_argument("--kind", choices=["geometric", "mandala", "kids", "infant"], default="geometric")
    p3.add_argument("--pages", type=int, default=20)
    p3.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p3.add_argument("--out", default="samples/coloring.pdf")

    # Notebook
    p4 = sub.add_parser("notebook", help="Generate notebook/journal")
    p4.add_argument("--title", required=True)
    p4.add_argument("--style", choices=["lined", "dotted", "blank"], default="lined")
    p4.add_argument("--pages", type=int, default=100)
    p4.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="6x9")
    p4.add_argument("--out", default="samples/notebook.pdf")

    # Worksheets: multiplication table
    p5 = sub.add_parser("multiplication", help="Generate multiplication table worksheets")
    p5.add_argument("--upto", type=int, default=10)
    p5.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p5.add_argument("--out", default="samples/multiplication.pdf")

    # Worksheets: simple arithmetic
    p6 = sub.add_parser("arithmetic", help="Generate simple arithmetic worksheets")
    p6.add_argument("--problems", type=int, default=50)
    p6.add_argument("--max", type=int, default=20)
    p6.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p6.add_argument("--out", default="samples/arithmetic.pdf")

    # Word search
    p7 = sub.add_parser("wordsearch", help="Generate word search puzzles")
    p7.add_argument("--size", type=int, default=12)
    p7.add_argument("--lang", choices=["pl", "en"], default="en")
    p7.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p7.add_argument("--out", default="samples/wordsearch.pdf")

    # Maze
    p8 = sub.add_parser("maze", help="Generate mazes")
    p8.add_argument("--size", type=int, default=15)
    p8.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p8.add_argument("--out", default="samples/maze.pdf")

    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    if args.command == "crossword":
        grid, words = generate_crossword(language=args.lang)
        render_crossword_pdf(grid, args.out, trim_size=args.trim, words=words)
        print(f"Saved crossword to {args.out}")
    elif args.command == "sudoku":
        puzzles = [make_puzzle(difficulty=args.difficulty) for _ in range(args.pages)]
        render_sudoku_pdf(puzzles, args.out, trim_size=args.trim)
        print(f"Saved sudoku to {args.out}")
    elif args.command == "coloring":
        render_coloring_pdf(args.kind, args.pages, args.out, trim_size=args.trim)
        print(f"Saved coloring pages to {args.out}")
    elif args.command == "notebook":
        render_notebook_pdf(args.title, args.pages, args.style, args.out, trim_size=args.trim)
        print(f"Saved notebook to {args.out}")
    elif args.command == "multiplication":
        render_multiplication_table_pdf(args.out, upto=args.upto, trim_size=args.trim)
        print(f"Saved multiplication worksheets to {args.out}")
    elif args.command == "arithmetic":
        render_simple_arithmetic_pdf(args.out, problems=args.problems, max_num=args.max, trim_size=args.trim)
        print(f"Saved arithmetic worksheets to {args.out}")
    elif args.command == "wordsearch":
        # reuse word lists
        from .crossword import load_wordlist
        words = load_wordlist(args.lang)[:20]
        render_word_search_pdf(args.out, words=words, size=args.size, trim_size=args.trim)
        print(f"Saved word search to {args.out}")
    elif args.command == "maze":
        render_maze_pdf(args.out, size=args.size, trim_size=args.trim)
        print(f"Saved maze to {args.out}")


if __name__ == "__main__":
    main()