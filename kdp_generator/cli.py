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
from .notebooks_extra import (
    render_grid_notebook_pdf,
    render_bullet_journal_pdf,
    render_daily_planner_pdf,
    render_monthly_planner_pdf,
    render_habit_tracker_pdf,
    render_budget_planner_pdf,
    render_recipe_book_pdf,
    render_herbarium_pdf,
)
from .thematic import (
    render_wedding_planner_pdf,
    render_teacher_planner_pdf,
    render_travel_journal_pdf,
    render_gratitude_journal_pdf,
    render_reading_log_pdf,
    render_meal_weekly_planner_pdf,
)
from .cover import render_kdp_cover_pdf


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

    # Extra notebooks & planners
    n1 = sub.add_parser("grid", help="Grid notebook")
    n1.add_argument("--title", default="Grid Notebook")
    n1.add_argument("--pages", type=int, default=120)
    n1.add_argument("--spacing", type=float, default=18.0)
    n1.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="6x9")
    n1.add_argument("--out", default="samples/grid_notebook.pdf")

    n2 = sub.add_parser("bujo", help="Bullet journal")
    n2.add_argument("--title", default="Bullet Journal")
    n2.add_argument("--pages", type=int, default=120)
    n2.add_argument("--spacing", type=float, default=18.0)
    n2.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="6x9")
    n2.add_argument("--out", default="samples/bujo.pdf")

    n3 = sub.add_parser("daily", help="Daily planner")
    n3.add_argument("--pages", type=int, default=90)
    n3.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    n3.add_argument("--out", default="samples/daily_planner.pdf")

    n4 = sub.add_parser("monthly_planner", help="Monthly undated planner")
    n4.add_argument("--months", type=int, default=12)
    n4.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    n4.add_argument("--out", default="samples/monthly_planner.pdf")

    n5 = sub.add_parser("habit", help="Habit tracker")
    n5.add_argument("--pages", type=int, default=12)
    n5.add_argument("--habits", type=int, default=10)
    n5.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    n5.add_argument("--out", default="samples/habit_tracker.pdf")

    n6 = sub.add_parser("budget", help="Budget planner")
    n6.add_argument("--pages", type=int, default=12)
    n6.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    n6.add_argument("--out", default="samples/budget_planner.pdf")

    n7 = sub.add_parser("recipe", help="Recipe book")
    n7.add_argument("--pages", type=int, default=100)
    n7.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    n7.add_argument("--out", default="samples/recipe_book.pdf")

    n8 = sub.add_parser("herbarium", help="Herbarium (pressed leaves)")
    n8.add_argument("--leaves", nargs="*", default=["Maple", "Oak", "Birch", "Chestnut", "Willow"])
    n8.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    n8.add_argument("--out", default="samples/herbarium.pdf")

    # Themed
    t1 = sub.add_parser("wedding", help="Wedding planner (rich layout)")
    t1.add_argument("--pages", type=int, default=20)
    t1.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    t1.add_argument("--out", default="samples/wedding_planner.pdf")

    t2 = sub.add_parser("teacher", help="Teacher planner (weeks + gradebook)")
    t2.add_argument("--weeks", type=int, default=40)
    t2.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    t2.add_argument("--out", default="samples/teacher_planner.pdf")

    t3 = sub.add_parser("travel", help="Travel journal (trips with daily logs)")
    t3.add_argument("--trips", type=int, default=6)
    t3.add_argument("--days", type=int, default=7)
    t3.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="6x9")
    t3.add_argument("--out", default="samples/travel_journal.pdf")

    t4 = sub.add_parser("gratitude", help="Gratitude journal (weekly prompts)")
    t4.add_argument("--weeks", type=int, default=52)
    t4.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="6x9")
    t4.add_argument("--out", default="samples/gratitude_journal.pdf")

    t5 = sub.add_parser("reading", help="Reading log")
    t5.add_argument("--entries", type=int, default=200)
    t5.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="6x9")
    t5.add_argument("--out", default="samples/reading_log.pdf")

    t6 = sub.add_parser("meal_weekly", help="Weekly meal planner")
    t6.add_argument("--weeks", type=int, default=52)
    t6.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="8.5x11")
    t6.add_argument("--out", default="samples/meal_weekly_planner.pdf")

    # Cover
    c1 = sub.add_parser("cover", help="Generate KDP full-wrap cover")
    c1.add_argument("--trim", choices=SUPPORTED_TRIM_SIZES, default="6x9")
    c1.add_argument("--pages", type=int, default=120)
    c1.add_argument("--stock", choices=["bw_55", "color_60"], default="bw_55")
    c1.add_argument("--bleed", action="store_true")
    c1.add_argument("--title", type=str, required=True)
    c1.add_argument("--subtitle", type=str, default="")
    c1.add_argument("--author", type=str, default="")
    c1.add_argument("--bg", type=str, default="#ffffff")
    c1.add_argument("--accent", type=str, default="#000000")
    c1.add_argument("--font", type=str, default="")
    c1.add_argument("--out", default="samples/cover.pdf")

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
    elif args.command == "grid":
        render_grid_notebook_pdf(args.title, args.pages, args.out, trim_size=args.trim, spacing=args.spacing)
        print(f"Saved grid notebook to {args.out}")
    elif args.command == "bujo":
        render_bullet_journal_pdf(args.title, args.pages, args.out, trim_size=args.trim, spacing=args.spacing)
        print(f"Saved bullet journal to {args.out}")
    elif args.command == "daily":
        render_daily_planner_pdf(args.pages, args.out, trim_size=args.trim)
        print(f"Saved daily planner to {args.out}")
    elif args.command == "monthly_planner":
        render_monthly_planner_pdf(args.months, args.out, trim_size=args.trim)
        print(f"Saved monthly planner to {args.out}")
    elif args.command == "habit":
        render_habit_tracker_pdf(args.pages, args.habits, args.out, trim_size=args.trim)
        print(f"Saved habit tracker to {args.out}")
    elif args.command == "budget":
        render_budget_planner_pdf(args.pages, args.out, trim_size=args.trim)
        print(f"Saved budget planner to {args.out}")
    elif args.command == "recipe":
        render_recipe_book_pdf(args.pages, args.out, trim_size=args.trim)
        print(f"Saved recipe book to {args.out}")
    elif args.command == "herbarium":
        render_herbarium_pdf(args.leaves, args.out, trim_size=args.trim)
        print(f"Saved herbarium to {args.out}")
    elif args.command == "wedding":
        render_wedding_planner_pdf(args.pages, args.out, trim_size=args.trim)
        print(f"Saved wedding planner to {args.out}")
    elif args.command == "teacher":
        render_teacher_planner_pdf(args.weeks, args.out, trim_size=args.trim)
        print(f"Saved teacher planner to {args.out}")
    elif args.command == "travel":
        render_travel_journal_pdf(args.trips, args.days, args.out, trim_size=args.trim)
        print(f"Saved travel journal to {args.out}")
    elif args.command == "gratitude":
        render_gratitude_journal_pdf(args.weeks, args.out, trim_size=args.trim)
        print(f"Saved gratitude journal to {args.out}")
    elif args.command == "reading":
        render_reading_log_pdf(args.entries, args.out, trim_size=args.trim)
        print(f"Saved reading log to {args.out}")
    elif args.command == "meal_weekly":
        render_meal_weekly_planner_pdf(args.weeks, args.out, trim_size=args.trim)
        print(f"Saved meal weekly planner to {args.out}")
    elif args.command == "cover":
        render_kdp_cover_pdf(
            args.out,
            trim_size=args.trim,
            page_count=args.pages,
            stock=args.stock,
            with_bleed=args.bleed,
            title=args.title,
            subtitle=(args.subtitle or None),
            author=(args.author or None),
            bg_color=args.bg,
            accent_color=args.accent,
            font_path=(args.font or None),
        )
        print(f"Saved KDP cover to {args.out}")


if __name__ == "__main__":
    main()