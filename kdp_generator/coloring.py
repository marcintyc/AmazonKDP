import random
from typing import List


def draw_geometric(canvas, page_width: float, page_height: float, margin: float):
    from reportlab.lib.colors import black
    canvas.setLineWidth(1)
    cols = 6
    rows = 8
    w = (page_width - 2 * margin) / cols
    h = (page_height - 2 * margin) / rows
    for i in range(cols):
        for j in range(rows):
            x = margin + i * w
            y = margin + j * h
            canvas.rect(x, y, w, h, stroke=1, fill=0)
            if (i + j) % 2 == 0:
                canvas.circle(x + w / 2, y + h / 2, min(w, h) * 0.3, stroke=1, fill=0)


def draw_mandala(canvas, page_width: float, page_height: float, margin: float):
    from math import cos, sin, pi
    canvas.setLineWidth(1)
    cx = page_width / 2
    cy = page_height / 2
    radius = min(page_width, page_height) / 2 - margin
    petals = 12
    rings = 6
    for r in range(1, rings + 1):
        pr = (r / rings) * radius
        canvas.circle(cx, cy, pr, stroke=1, fill=0)
        for p in range(petals):
            angle = (2 * pi * p) / petals
            x1 = cx + pr * cos(angle)
            y1 = cy + pr * sin(angle)
            x2 = cx + pr * cos(angle + pi / petals)
            y2 = cy + pr * sin(angle + pi / petals)
            canvas.line(x1, y1, x2, y2)


def render_coloring_pdf(kind: str, pages: int, filename: str, trim_size: str = "8.5x11"):
    from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    for i in range(1, pages + 1):
        if kind == "mandala":
            draw_mandala(canvas, page_width, page_height, margin)
        else:
            draw_geometric(canvas, page_width, page_height, margin)
        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()