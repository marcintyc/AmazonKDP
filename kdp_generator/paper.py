from typing import Tuple
from reportlab.lib.colors import Color
from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number


def render_graph_paper_pdf(filename: str, spacing_inch: float = 0.25, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.5 * 72

    light = Color(0.3, 0.5, 0.9, alpha=1)
    dark = Color(0.15, 0.3, 0.7, alpha=1)

    canvas.setLineWidth(0.5)
    step = spacing_inch * 72
    x = margin
    idx = 0
    while x <= page_width - margin:
        canvas.setStrokeColor(dark if idx % 4 == 0 else light)
        canvas.line(x, margin, x, page_height - margin)
        x += step
        idx += 1
    y = margin
    idx = 0
    while y <= page_height - margin:
        canvas.setStrokeColor(dark if idx % 4 == 0 else light)
        canvas.line(margin, y, page_width - margin, y)
        y += step
        idx += 1

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_isometric_paper_pdf(filename: str, triangle_side_inch: float = 0.25, trim_size: str = "8.5x11"):
    from math import sqrt
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.5 * 72

    side = triangle_side_inch * 72
    h = sqrt(3) / 2 * side

    canvas.setLineWidth(0.4)
    canvas.setStrokeColor(Color(0.2, 0.6, 0.6, 1))

    y = margin
    row = 0
    while y <= page_height - margin:
        x = margin - (side / 2 if row % 2 else 0)
        while x <= page_width - margin + side:
            # draw small triangle edges
            canvas.line(x, y, x + side / 2, y + h)
            canvas.line(x + side / 2, y + h, x + side, y)
            canvas.line(x, y, x + side, y)
            x += side
        y += h
        row += 1

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()


def render_music_staff_paper_pdf(filename: str, staves_per_page: int = 8, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    staff_gap = (page_height - 2 * margin) / staves_per_page
    line_spacing = staff_gap / 8

    canvas.setLineWidth(1)

    y = page_height - margin
    for s in range(staves_per_page):
        # center 5 lines vertically within staff_gap
        start_y = y - line_spacing * 4
        for i in range(5):
            yy = start_y - i * line_spacing
            canvas.line(margin, yy, page_width - margin, yy)
        y -= staff_gap

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()