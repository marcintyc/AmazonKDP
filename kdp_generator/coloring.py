import random
from typing import List


def draw_geometric(canvas, page_width: float, page_height: float, margin: float):
    canvas.setLineWidth(1.5)
    cols = random.choice([5, 6, 7])
    rows = random.choice([6, 7, 8])
    w = (page_width - 2 * margin) / cols
    h = (page_height - 2 * margin) / rows
    for i in range(cols):
        for j in range(rows):
            x = margin + i * w
            y = margin + j * h
            canvas.rect(x, y, w, h, stroke=1, fill=0)
            # random inner decoration
            r = random.random()
            if r < 0.33:
                canvas.circle(x + w / 2, y + h / 2, min(w, h) * 0.3, stroke=1, fill=0)
            elif r < 0.66:
                canvas.line(x, y, x + w, y + h)
                canvas.line(x + w, y, x, y + h)
            else:
                canvas.ellipse(x + w * 0.2, y + h * 0.2, x + w * 0.8, y + h * 0.8, stroke=1, fill=0)


def draw_mandala(canvas, page_width: float, page_height: float, margin: float):
    from math import cos, sin, pi
    cx = page_width / 2
    cy = page_height / 2
    radius = min(page_width, page_height) / 2 - margin
    petals = random.randint(10, 24)
    rings = random.randint(5, 10)
    base_angle = random.random() * 2 * pi

    for r in range(1, rings + 1):
        pr = (r / rings) * radius
        canvas.setLineWidth(1 + (r % 3 == 0))
        # ring
        canvas.circle(cx, cy, pr, stroke=1, fill=0)
        # spokes and motifs
        for p in range(petals):
            angle = base_angle + (2 * pi * p) / petals
            x1 = cx + pr * cos(angle)
            y1 = cy + pr * sin(angle)
            x2 = cx + pr * cos(angle + pi / petals)
            y2 = cy + pr * sin(angle + pi / petals)
            if r % 2 == 0:
                canvas.line(x1, y1, x2, y2)
            else:
                # small diamond/leaf
                x3 = cx + (pr * 0.85) * cos(angle + pi / (2 * petals))
                y3 = cy + (pr * 0.85) * sin(angle + pi / (2 * petals))
                canvas.line(x1, y1, x3, y3)
                canvas.line(x3, y3, x2, y2)
        # occasional star polygon
        if r % 3 == 0:
            for p in range(petals):
                a1 = base_angle + (2 * pi * p) / petals
                a2 = base_angle + (2 * pi * ((p + 2) % petals)) / petals
                x1 = cx + pr * cos(a1)
                y1 = cy + pr * sin(a1)
                x2 = cx + pr * cos(a2)
                y2 = cy + pr * sin(a2)
                canvas.line(x1, y1, x2, y2)


def draw_kids_simple(canvas, page_width: float, page_height: float, margin: float):
    # High-contrast big shapes with thick outlines for small children
    from math import cos, sin, pi
    canvas.setLineWidth(4)
    num = random.randint(3, 6)
    for _ in range(num):
        shape = random.choice(["circle", "square", "triangle", "star", "heart"])
        w = random.uniform(1.5, 3.0) * 72
        h = w
        x = random.uniform(margin, page_width - margin - w)
        y = random.uniform(margin, page_height - margin - h)
        if shape == "circle":
            canvas.circle(x + w / 2, y + h / 2, min(w, h) / 2, stroke=1, fill=0)
        elif shape == "square":
            canvas.rect(x, y, w, h, stroke=1, fill=0)
        elif shape == "triangle":
            canvas.line(x + w / 2, y + h, x, y)
            canvas.line(x, y, x + w, y)
            canvas.line(x + w, y, x + w / 2, y + h)
        elif shape == "star":
            # simple 5-point star
            R = w / 2
            r = R * 0.5
            cx = x + w / 2
            cy = y + h / 2
            pts = []
            for i in range(10):
                ang = -pi / 2 + i * pi / 5
                rad = R if i % 2 == 0 else r
                pts.append((cx + rad * cos(ang), cy + rad * sin(ang)))
            for i in range(10):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % 10]
                canvas.line(x1, y1, x2, y2)
        elif shape == "heart":
            # approximate heart using arcs and lines
            cx = x + w / 2
            cy = y + h * 0.55
            canvas.circle(cx - w * 0.25, cy, w * 0.25)
            canvas.circle(cx + w * 0.25, cy, w * 0.25)
            canvas.line(cx - w * 0.5, cy, cx, y)
            canvas.line(cx + w * 0.5, cy, cx, y)


def draw_infant_high_contrast(canvas, page_width: float, page_height: float, margin: float):
    # Science-informed: infants 0-6m respond best to bold black-white high-contrast shapes
    from math import cos, sin, pi
    canvas.setLineWidth(6)
    cx = page_width / 2
    cy = page_height / 2
    mode = random.choice(["bullseye", "checker", "stripes", "zigzag", "targets"])
    if mode == "bullseye":
        R = min(page_width, page_height) / 2 - margin
        bands = random.randint(5, 9)
        for i in range(bands):
            r = R * (1 - i / bands)
            canvas.circle(cx, cy, r, stroke=1, fill=0)
    elif mode == "checker":
        cols = rows = random.choice([6, 8, 10])
        w = (page_width - 2 * margin) / cols
        h = (page_height - 2 * margin) / rows
        for i in range(cols):
            for j in range(rows):
                x = margin + i * w
                y = margin + j * h
                if (i + j) % 2 == 0:
                    canvas.rect(x, y, w, h, stroke=1, fill=0)
                else:
                    canvas.rect(x, y, w, h, stroke=1, fill=0)
    elif mode == "stripes":
        stripes = random.randint(6, 12)
        w = (page_width - 2 * margin) / stripes
        for i in range(stripes):
            x = margin + i * w
            canvas.rect(x, margin, w, page_height - 2 * margin, stroke=1, fill=0)
    elif mode == "zigzag":
        steps = 20
        x0 = margin
        y = margin
        step_x = (page_width - 2 * margin) / steps
        up = True
        for i in range(steps):
            x1 = x0 + step_x
            y1 = page_height - margin if up else margin
            canvas.line(x0, y, x1, y1)
            x0, y = x1, y1
            up = not up
    else:  # targets
        targets = random.randint(3, 6)
        for _ in range(targets):
            r = random.uniform(1.0, 2.5) * 72
            x = random.uniform(margin + r, page_width - margin - r)
            y = random.uniform(margin + r, page_height - margin - r)
            rings = random.randint(3, 6)
            for k in range(rings):
                canvas.circle(x, y, r * (k + 1) / rings)


def render_coloring_pdf(kind: str, pages: int, filename: str, trim_size: str = "8.5x11"):
    from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    for i in range(1, pages + 1):
        if kind == "mandala":
            draw_mandala(canvas, page_width, page_height, margin)
        elif kind == "kids":
            draw_kids_simple(canvas, page_width, page_height, margin)
        elif kind == "infant":
            draw_infant_high_contrast(canvas, page_width, page_height, margin)
        else:
            draw_geometric(canvas, page_width, page_height, margin)
        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()