import calendar as _cal
import datetime
import random
from typing import List

from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number


def render_connect_the_dots_pdf(filename: str, pages: int = 20, num_points: int = 40, trim_size: str = "8.5x11"):
    from math import sin, cos, pi
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    for p in range(1, pages + 1):
        # create a parametric shape path (circle/star/spiral)
        mode = random.choice(["circle", "star", "spiral", "polygon"])
        pts = []
        cx, cy = page_width / 2, page_height / 2
        R = min(page_width, page_height) / 2 - margin
        n = num_points
        if mode == "circle":
            for i in range(n):
                a = 2 * pi * i / n
                pts.append((cx + R * 0.6 * cos(a), cy + R * 0.6 * sin(a)))
        elif mode == "star":
            k = random.choice([5, 6, 7])
            for i in range(n):
                a = 2 * pi * i / n
                r = R * (0.3 if (i % 2) else 0.6)
                pts.append((cx + r * cos(a), cy + r * sin(a)))
        elif mode == "spiral":
            a0 = random.uniform(0.2, 0.5)
            for i in range(n):
                a = 2 * pi * i / (n / 2)
                r = R * (i / n) * 0.7
                pts.append((cx + r * cos(a + a0), cy + r * sin(a + a0)))
        else:  # polygon
            k = random.randint(5, 10)
            ang0 = random.random() * 2 * pi
            for i in range(k):
                a = ang0 + 2 * pi * i / k
                pts.append((cx + R * 0.6 * cos(a), cy + R * 0.6 * sin(a)))
            # resample along edges to get ~n points
            fine = []
            each = max(1, n // len(pts))
            for i in range(len(pts)):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % len(pts)]
                for t in range(each):
                    u = t / each
                    fine.append((x1 * (1 - u) + x2 * u, y1 * (1 - u) + y2 * u))
            pts = fine[:n]
        # draw dots with numbers
        canvas.setFont("Helvetica", 10)
        for i, (x, y) in enumerate(pts, start=1):
            canvas.circle(x, y, 2, stroke=1, fill=0)
            canvas.drawString(x + 4, y + 2, str(i))
        draw_footer_page_number(canvas, page_width, margin, p)
        canvas.showPage()
    canvas.save()


def render_tracing_letters_pdf(filename: str, pages: int = 10, text: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    rows = 10
    line_h = (page_height - 2 * margin) / rows
    base_y = page_height - margin - line_h * 0.7

    for p in range(1, pages + 1):
        canvas.setFont("Helvetica", 48)
        x = margin
        y = base_y
        for r in range(rows):
            # baseline
            canvas.setLineWidth(0.5)
            canvas.line(margin, y - 10, page_width - margin, y - 10)
            # letters across the line
            for ch in text:
                canvas.setFillGray(0.7)
                canvas.drawString(x, y, ch)
                x += 28
                if x > page_width - margin - 28:
                    break
            x = margin
            y -= line_h
        draw_footer_page_number(canvas, page_width, margin, p)
        canvas.showPage()
    canvas.save()


def render_monthly_calendar_pdf(filename: str, year: int = None, month: int = None, trim_size: str = "8.5x11"):
    import datetime
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    if year is None or month is None:
        today = datetime.date.today()
        year, month = today.year, today.month

    cal = _cal.monthcalendar(year, month)

    title = f"{_cal.month_name[month]} {year}"
    canvas.setFont("Helvetica-Bold", 24)
    tw = canvas.stringWidth(title, "Helvetica-Bold", 24)
    canvas.drawString((page_width - tw) / 2, page_height - margin - 10, title)

    rows = len(cal)
    cols = 7
    grid_w = page_width - 2 * margin
    grid_h = page_height - 2 * margin - 40
    cell_w = grid_w / cols
    cell_h = grid_h / rows

    # draw grid and day numbers
    canvas.setFont("Helvetica", 12)
    for r in range(rows):
        for c in range(cols):
            x = margin + c * cell_w
            y = margin + (rows - 1 - r) * cell_h
            canvas.rect(x, y, cell_w, cell_h, stroke=1, fill=0)
            d = cal[r][c]
            if d != 0:
                canvas.drawString(x + 4, y + cell_h - 14, str(d))

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_weekly_planner_pdf(filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = 7
    rows = 12
    grid_w = page_width - 2 * margin
    grid_h = page_height - 2 * margin
    cell_w = grid_w / cols
    cell_h = grid_h / rows

    canvas.setFont("Helvetica-Bold", 16)
    for c, day in enumerate(days):
        x = margin + c * cell_w
        y = page_height - margin
        canvas.drawString(x + 4, y - 18, day)

    # grid
    canvas.setLineWidth(0.8)
    for r in range(rows + 1):
        y = margin + r * cell_h
        canvas.line(margin, y, margin + grid_w, y)
    for c in range(cols + 1):
        x = margin + c * cell_w
        canvas.line(x, margin, x, margin + grid_h)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()