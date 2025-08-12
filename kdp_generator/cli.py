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
from .paper import render_graph_paper_pdf, render_isometric_paper_pdf, render_music_staff_paper_pdf
from .education import (
    render_connect_the_dots_pdf,
    render_tracing_letters_pdf,
    render_monthly_calendar_pdf,
    render_weekly_planner_pdf,
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

    # Paper
    p9 = sub.add_parser("graph", help="Generate graph paper")
    p9.add_argument("--spacing", type=float, default=0.25)
    p9.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p9.add_argument("--out", default="samples/graph.pdf")

    p10 = sub.add_parser("isometric", help="Generate isometric paper")
    p10.add_argument("--side", type=float, default=0.25)
    p10.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p10.add_argument("--out", default="samples/isometric.pdf")

    p11 = sub.add_parser("music", help="Generate music staff paper")
    p11.add_argument("--staves", type=int, default=8)
    p11.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p11.add_argument("--out", default="samples/music.pdf")

    # Education
    p12 = sub.add_parser("dots", help="Generate connect-the-dots pages")
    p12.add_argument("--pages", type=int, default=20)
    p12.add_argument("--points", type=int, default=40)
    p12.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p12.add_argument("--out", default="samples/dots.pdf")

    p13 = sub.add_parser("tracing", help="Generate letter tracing pages")
    p13.add_argument("--pages", type=int, default=10)
    p13.add_argument("--text", type=str, default="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    p13.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p13.add_argument("--out", default="samples/tracing.pdf")

    p14 = sub.add_parser("calendar", help="Generate monthly calendar")
    p14.add_argument("--year", type=int, default=0)
    p14.add_argument("--month", type=int, default=0)
    p14.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p14.add_argument("--out", default="samples/calendar.pdf")

    p15 = sub.add_parser("weekly", help="Generate weekly planner")
    p15.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    p15.add_argument("--out", default="samples/weekly.pdf")

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
        from .crossword import load_wordlist
        words = load_wordlist(args.lang)[:20]
        render_word_search_pdf(args.out, words=words, size=args.size, trim_size=args.trim)
        print(f"Saved word search to {args.out}")
    elif args.command == "maze":
        render_maze_pdf(args.out, size=args.size, trim_size=args.trim)
        print(f"Saved maze to {args.out}")
    elif args.command == "graph":
        render_graph_paper_pdf(args.out, spacing_inch=args.spacing, trim_size=args.trim)
        print(f"Saved graph paper to {args.out}")
    elif args.command == "isometric":
        render_isometric_paper_pdf(args.out, triangle_side_inch=args.side, trim_size=args.trim)
        print(f"Saved isometric paper to {args.out}")
    elif args.command == "music":
        render_music_staff_paper_pdf(args.out, staves_per_page=args.staves, trim_size=args.trim)
        print(f"Saved music staff paper to {args.out}")
    elif args.command == "dots":
        render_connect_the_dots_pdf(args.out, pages=args.pages, num_points=args.points, trim_size=args.trim)
        print(f"Saved connect-the-dots to {args.out}")
    elif args.command == "tracing":
        render_tracing_letters_pdf(args.out, pages=args.pages, text=args.text, trim_size=args.trim)
        print(f"Saved tracing pages to {args.out}")
    elif args.command == "calendar":
        y = None if args.year == 0 else args.year
        m = None if args.month == 0 else args.month
        render_monthly_calendar_pdf(args.out, year=y, month=m, trim_size=args.trim)
        print(f"Saved monthly calendar to {args.out}")
    elif args.command == "weekly":
        render_weekly_planner_pdf(args.out, trim_size=args.trim)
        print(f"Saved weekly planner to {args.out}")


if __name__ == "__main__":
    main()