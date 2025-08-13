from typing import List, Literal
from reportlab.lib.colors import black, HexColor, Color
from .pdf_utils import create_canvas, size_to_points, draw_centered_title, draw_footer_page_number, draw_dot_grid


def _page_setup(trim_size: str):
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72
    return page_width, page_height, margin


def render_grid_notebook_pdf(title: str, pages: int, filename: str, trim_size: str = "6x9", spacing: float = 18.0):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    canvas.setFillColor(HexColor("#e2f0ff"))
    canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    canvas.setFillColor(black)
    draw_centered_title(canvas, page_width, page_height, title, y_ratio=0.7, font_size=40)
    canvas.showPage()

    for i in range(1, pages + 1):
        canvas.setLineWidth(0.4)
        x = margin
        while x <= page_width - margin:
            canvas.setStrokeColor(Color(0.7, 0.8, 0.9))
            canvas.line(x, margin, x, page_height - margin)
            x += spacing
        y = margin
        while y <= page_height - margin:
            canvas.setStrokeColor(Color(0.7, 0.8, 0.9))
            canvas.line(margin, y, page_width - margin, y)
            y += spacing
        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()


def render_bullet_journal_pdf(title: str, pages: int, filename: str, trim_size: str = "6x9", spacing: float = 14.4):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    canvas.setFillColor(HexColor("#fff7ed"))
    canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    canvas.setFillColor(black)
    draw_centered_title(canvas, page_width, page_height, title, y_ratio=0.7, font_size=40)
    canvas.showPage()

    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawString(margin, page_height - margin - 20, "Index")
    canvas.setFont("Helvetica", 12)
    y = page_height - margin - 50
    for i in range(1, 30):
        canvas.drawString(margin, y, f"{i:02d}. .............................................  p. ")
        y -= 18
    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()

    for p in range(2):
        canvas.setFont("Helvetica-Bold", 16)
        cols = 3
        col_w = (page_width - 2 * margin) / cols
        for c in range(cols):
            x = margin + c * col_w
            canvas.drawString(x, page_height - margin - 20, "Month")
            yy = page_height - margin - 40
            for _ in range(12):
                canvas.setFont("Helvetica", 11)
                canvas.drawString(x, yy, "- ")
                yy -= 14
        draw_footer_page_number(canvas, page_width, margin, 2 + p)
        canvas.showPage()

    for i in range(1, pages + 1):
        draw_dot_grid(canvas, page_width, page_height, margin, spacing=spacing, radius=0.8, gray=0.75)
        draw_footer_page_number(canvas, page_width, margin, 4 + i)
        canvas.showPage()
    canvas.save()


def render_daily_planner_pdf(pages: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    for i in range(1, pages + 1):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, "Daily Planner")
        canvas.setFont("Helvetica", 12)
        canvas.drawString(page_width - margin - 200, page_height - margin - 10, "Date: __________")

        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(margin, page_height - margin - 40, "Top Priorities")
        y = page_height - margin - 60
        for _ in range(3):
            canvas.rect(margin, y - 8, page_width - 2 * margin, 18, stroke=1, fill=0)
            y -= 24

        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(margin, page_height - margin - 150, "Schedule")
        y = page_height - margin - 170
        for hour in range(6, 23):
            canvas.setFont("Helvetica", 11)
            canvas.drawString(margin, y, f"{hour:02d}:00")
            canvas.line(margin + 60, y + 2, page_width - margin, y + 2)
            y -= 22

        canvas.setFont("Helvetica-Bold", 14)
        x0 = page_width / 2 + 20
        yt = page_height - margin - 150
        canvas.drawString(x0, page_height - margin - 150, "To-Do")
        yt -= 20
        for _ in range(18):
            canvas.rect(x0, yt - 8, 12, 12, stroke=1, fill=0)
            canvas.line(x0 + 20, yt - 2, page_width - margin, yt - 2)
            yt -= 22

        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()


def render_monthly_planner_pdf(months: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    cols, rows = 7, 6
    grid_w = page_width - 2 * margin
    grid_h = page_height - 2 * margin - 40
    cell_w = grid_w / cols
    cell_h = grid_h / rows

    for i in range(1, months + 1):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, "Monthly Planner")
        for r in range(rows + 1):
            y = margin + r * cell_h
            canvas.line(margin, y, margin + grid_w, y)
        for c in range(cols + 1):
            x = margin + c * cell_w
            canvas.line(x, margin, x, margin + grid_h)
        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()


def render_habit_tracker_pdf(pages: int, habits: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    cols = 31
    rows = habits + 1
    grid_w = page_width - 2 * margin
    grid_h = page_height - 2 * margin - 40
    cell_w = grid_w / (cols + 1)
    cell_h = grid_h / rows

    for i in range(1, pages + 1):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, "Habit Tracker")

        canvas.setFont("Helvetica", 10)
        for d in range(1, cols + 1):
            x = margin + (d + 0) * cell_w
            canvas.drawCentredString(x + cell_w / 2, page_height - margin - 30, str(d))

        for r in range(rows + 1):
            y = margin + r * cell_h
            canvas.line(margin, y, margin + grid_w, y)
        for c in range(cols + 2):
            x = margin + c * cell_w
            canvas.line(x, margin, x, margin + grid_h)

        y = margin + grid_h - cell_h + 6
        for _ in range(habits):
            canvas.line(margin + 6, y, margin + cell_w - 6, y)
            y -= cell_h

        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()


def render_budget_planner_pdf(pages: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    for i in range(1, pages + 1):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, "Budget Planner")
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(margin, page_height - margin - 40, "Income")
        y = page_height - margin - 60
        for _ in range(6):
            canvas.rect(margin, y - 10, page_width - 2 * margin, 20, stroke=1, fill=0)
            y -= 24
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(margin, y - 20, "Expenses")
        y -= 40
        for _ in range(16):
            canvas.rect(margin, y - 10, page_width - 2 * margin, 20, stroke=1, fill=0)
            y -= 24
        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()


def render_recipe_book_pdf(pages: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    for i in range(1, pages + 1):
        canvas.setFont("Helvetica-Bold", 20)
        canvas.drawString(margin, page_height - margin - 10, "Recipe")
        canvas.setFont("Helvetica", 12)
        canvas.drawString(margin, page_height - margin - 40, "Title: ___________________________")
        canvas.drawString(margin, page_height - margin - 60, "Prep Time: ______  Cook Time: ______  Servings: ______")

        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(margin, page_height - margin - 90, "Ingredients")
        y = page_height - margin - 110
        for _ in range(15):
            canvas.rect(margin, y - 8, page_width / 2 - margin - 10, 18, stroke=1, fill=0)
            y -= 20

        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(page_width / 2 + 10, page_height - margin - 90, "Directions")
        y = page_height - margin - 110
        for _ in range(20):
            canvas.line(page_width / 2 + 10, y, page_width - margin, y)
            y -= 18

        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()


def render_herbarium_pdf(leaves: List[str], filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _page_setup(trim_size)

    canvas.setFillColor(HexColor("#f0fdf4"))
    canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    canvas.setFillColor(black)
    draw_centered_title(canvas, page_width, page_height, "Herbarium", y_ratio=0.7, font_size=48)
    canvas.showPage()

    canvas.setFont("Helvetica-Bold", 22)
    canvas.drawString(margin, page_height - margin - 10, "Table of Contents")
    canvas.setFont("Helvetica", 12)
    y = page_height - margin - 40
    page_start = 3
    for idx, leaf in enumerate(leaves, start=0):
        canvas.drawString(margin, y, f"{idx+1:02d}. {leaf}  ..........  p. {page_start + idx}")
        y -= 16
        if y < margin + 20:
            canvas.showPage()
            canvas.setFont("Helvetica", 12)
            y = page_height - margin - 40
    canvas.showPage()

    for i, leaf in enumerate(leaves, start=1):
        canvas.setFont("Helvetica-Bold", 24)
        canvas.drawString(margin, page_height - margin - 20, leaf)
        canvas.setFont("Helvetica", 12)
        canvas.drawString(margin, page_height - margin - 40, "Collected on: __________   Location: __________")
        x = margin
        y = margin + 40
        w = page_width - 2 * margin
        h = page_height - 2 * margin - 100
        canvas.setLineWidth(2)
        canvas.rect(x, y, w, h, stroke=1, fill=0)
        canvas.setFont("Helvetica", 12)
        canvas.drawString(margin, y - 20, "Notes:")
        draw_footer_page_number(canvas, page_width, margin, 2 + i)
        canvas.showPage()
    canvas.save()