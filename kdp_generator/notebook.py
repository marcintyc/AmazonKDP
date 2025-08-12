from typing import Literal

from reportlab.lib.colors import black, HexColor

from .pdf_utils import create_canvas, size_to_points, draw_centered_title, draw_footer_page_number

PageStyle = Literal["lined", "dotted", "blank"]


def draw_lined_page(canvas, page_width: float, page_height: float, margin: float, line_spacing: float = 24.0):
    y = margin
    canvas.setLineWidth(0.5)
    while y < page_height - margin:
        canvas.setStrokeColor(black)
        canvas.line(margin, y, page_width - margin, y)
        y += line_spacing


def draw_dotted_page(canvas, page_width: float, page_height: float, margin: float, spacing: float = 24.0):
    x = margin
    y = margin
    r = 0.8
    while y < page_height - margin:
        x = margin
        while x < page_width - margin:
            canvas.circle(x, y, r, stroke=1, fill=0)
            x += spacing
        y += spacing


def render_notebook_pdf(title: str, pages: int, style: PageStyle, filename: str, trim_size: str = "6x9"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = 0.75 * 72

    # Cover page
    canvas.setFillColor(HexColor("#f2f2f2"))
    canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    canvas.setFillColor(black)
    draw_centered_title(canvas, page_width, page_height, title, y_ratio=0.7, font_size=40)
    canvas.setFont("Helvetica", 16)
    subtitle = "Notebook / Journal"
    tw = canvas.stringWidth(subtitle, "Helvetica", 16)
    canvas.drawString((page_width - tw) / 2, page_height * 0.65, subtitle)
    canvas.showPage()

    # Interior pages
    for i in range(1, pages + 1):
        if style == "dotted":
            draw_dotted_page(canvas, page_width, page_height, margin)
        elif style == "blank":
            pass
        else:
            draw_lined_page(canvas, page_width, page_height, margin)
        draw_footer_page_number(canvas, page_width, margin, i)
        canvas.showPage()
    canvas.save()