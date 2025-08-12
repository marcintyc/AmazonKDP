from typing import List
from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number


def _setup(trim_size: str):
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72
    return page_width, page_height, margin


def render_wedding_planner_pdf(pages: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _setup(trim_size)

    for i in range(1, pages + 1):
        y = page_height - margin - 10
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, y, "Wedding Planner")
        y -= 24
        canvas.setFont("Helvetica-Bold", 14)
        sections = [
            ("Checklist", 10), ("Budget", 8), ("Guest List", 10), ("Vendors", 10), ("Timeline", 8)
        ]
        col = 0
        col_w = (page_width - 2 * margin) / 2
        for title, lines in sections:
            x = margin + col * col_w
            if y < margin + 120:
                col += 1
                y = page_height - margin - 40
                if col == 2:
                    draw_footer_page_number(canvas, page_width, margin, i)
                    canvas.showPage()
                    y = page_height - margin - 10
                    canvas.setFont("Helvetica-Bold", 18)
                    canvas.drawString(margin, y, "Wedding Planner")
                    y -= 24
                    canvas.setFont("Helvetica-Bold", 14)
                    col = 0
                    x = margin
            canvas.drawString(x, y, title)
            y -= 12
            canvas.setFont("Helvetica", 11)
            for _ in range(lines):
                canvas.rect(x, y - 10, col_w - 16, 18, stroke=1, fill=0)
                y -= 20
            y -= 8
            canvas.setFont("Helvetica-Bold", 14)
        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()


def render_teacher_planner_pdf(weeks: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _setup(trim_size)

    # Weekly lesson planning pages
    for w in range(1, weeks + 1):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, f"Teacher Planner — Week {w}")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        periods = 8
        grid_w = page_width - 2 * margin
        grid_h = page_height - 2 * margin - 40
        cell_w = grid_w / len(days)
        cell_h = grid_h / (periods + 1)
        canvas.setFont("Helvetica-Bold", 12)
        for c, d in enumerate(days):
            x = margin + c * cell_w
            canvas.drawCentredString(x + cell_w / 2, page_height - margin - 30, d)
        # grid
        for r in range(periods + 2):
            y = margin + r * cell_h
            canvas.line(margin, y, margin + grid_w, y)
        for c in range(len(days) + 1):
            x = margin + c * cell_w
            canvas.line(x, margin, x, margin + grid_h)
        draw_footer_page_number(canvas, page_width, margin, w)
        canvas.showPage()

    # Grade book pages
    for p in range(1, 6):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, "Grade Book")
        students = 25
        assignments = 10
        grid_w = page_width - 2 * margin
        grid_h = page_height - 2 * margin - 40
        cell_w = grid_w / (assignments + 1)
        cell_h = grid_h / (students + 1)
        # headers
        canvas.setFont("Helvetica", 10)
        for a in range(assignments):
            x = margin + (a + 1) * cell_w
            canvas.drawCentredString(x + cell_w / 2, page_height - margin - 30, f"A{a+1}")
        # grid
        for r in range(students + 2):
            y = margin + r * cell_h
            canvas.line(margin, y, margin + grid_w, y)
        for c in range(assignments + 2):
            x = margin + c * cell_w
            canvas.line(x, margin, x, margin + grid_h)
        draw_footer_page_number(canvas, page_width, margin, weeks + p)
        canvas.showPage()
    canvas.save()


def render_travel_journal_pdf(trips: int, days_per_trip: int, filename: str, trim_size: str = "6x9"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _setup(trim_size)

    page_num = 1
    for t in range(1, trips + 1):
        # Trip summary
        canvas.setFont("Helvetica-Bold", 20)
        canvas.drawString(margin, page_height - margin - 10, f"Trip {t}")
        canvas.setFont("Helvetica", 12)
        y = page_height - margin - 40
        fields = ["Destination", "Dates", "Budget", "Companions", "Highlights"]
        for f in fields:
            canvas.drawString(margin, y, f"{f}: _________________________________")
            y -= 20
        canvas.drawString(margin, y - 10, "Itinerary:")
        y -= 30
        for _ in range(10):
            canvas.line(margin, y, page_width - margin, y)
            y -= 16
        draw_footer_page_number(canvas, page_width, margin, page_num)
        canvas.showPage()
        page_num += 1

        # Daily logs
        for d in range(1, days_per_trip + 1):
            canvas.setFont("Helvetica-Bold", 16)
            canvas.drawString(margin, page_height - margin - 10, f"Day {d}")
            canvas.setFont("Helvetica", 12)
            y = page_height - margin - 40
            canvas.drawString(margin, y, "Morning:")
            y -= 20
            for _ in range(6):
                canvas.line(margin, y, page_width - margin, y)
                y -= 16
            canvas.drawString(margin, y - 4, "Afternoon:")
            y -= 24
            for _ in range(6):
                canvas.line(margin, y, page_width - margin, y)
                y -= 16
            canvas.drawString(margin, y - 4, "Evening:")
            y -= 24
            for _ in range(6):
                canvas.line(margin, y, page_width - margin, y)
                y -= 16
            draw_footer_page_number(canvas, page_width, margin, page_num)
            canvas.showPage()
            page_num += 1
    canvas.save()


def render_gratitude_journal_pdf(weeks: int, filename: str, trim_size: str = "6x9"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _setup(trim_size)

    page_num = 1
    for w in range(1, weeks + 1):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, f"Week {w}")
        prompts = [
            "Today I am grateful for...",
            "This made me smile...",
            "A small win today...",
            "Someone I appreciate is...",
            "I will make tomorrow better by...",
        ]
        y = page_height - margin - 40
        canvas.setFont("Helvetica", 12)
        for q in prompts:
            canvas.drawString(margin, y, q)
            y -= 18
            for _ in range(6):
                canvas.line(margin, y, page_width - margin, y)
                y -= 16
            y -= 8
        draw_footer_page_number(canvas, page_width, margin, page_num)
        canvas.showPage()
        page_num += 1
    canvas.save()


def render_reading_log_pdf(entries: int, filename: str, trim_size: str = "6x9"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _setup(trim_size)

    page_num = 1
    per_page = 6
    total_pages = (entries + per_page - 1) // per_page
    idx = 0
    for p in range(total_pages):
        y = page_height - margin - 10
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, y, "Reading Log")
        y -= 24
        canvas.setFont("Helvetica", 12)
        for _ in range(min(per_page, entries - idx)):
            fields = [
                "Title", "Author", "Start Date", "Finish Date", "Rating (1-5)", "Review"
            ]
            for f in fields[:-1]:
                canvas.drawString(margin, y, f"{f}: ______________________________")
                y -= 18
            canvas.drawString(margin, y, "Review:")
            y -= 18
            for _ in range(4):
                canvas.line(margin, y, page_width - margin, y)
                y -= 16
            y -= 8
            idx += 1
        draw_footer_page_number(canvas, page_width, margin, page_num)
        canvas.showPage()
        page_num += 1
    canvas.save()


def render_meal_weekly_planner_pdf(weeks: int, filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height, margin = _setup(trim_size)

    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    for w in range(1, weeks + 1):
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(margin, page_height - margin - 10, f"Weekly Meal Planner — Week {w}")
        cols = 7
        rows = 3  # Breakfast, Lunch, Dinner
        grid_w = page_width - 2 * margin
        grid_h = (page_height - 2 * margin) * 0.6
        cell_w = grid_w / cols
        cell_h = grid_h / (rows + 1)
        # headers
        canvas.setFont("Helvetica-Bold", 12)
        for c, d in enumerate(days):
            x = margin + c * cell_w
            canvas.drawCentredString(x + cell_w / 2, page_height - margin - 30, d)
        labels = ["Breakfast","Lunch","Dinner"]
        for r, lab in enumerate(labels, start=1):
            y = margin + grid_h - r * cell_h + 6
            canvas.drawString(margin - 2, y + 8, lab)
        # grid
        for r in range(rows + 2):
            y = margin + r * cell_h
            canvas.line(margin, y, margin + grid_w, y)
        for c in range(cols + 1):
            x = margin + c * cell_w
            canvas.line(x, margin, x, margin + grid_h)

        # Grocery list
        x0 = margin
        y0 = margin + grid_h + 30
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(x0, y0, "Grocery List")
        y = y0 - 16
        for _ in range(18):
            canvas.rect(x0, y - 8, page_width - 2 * margin, 16, stroke=1, fill=0)
            y -= 18

        draw_footer_page_number(canvas, page_width, margin, w)
        canvas.showPage()
    canvas.save()