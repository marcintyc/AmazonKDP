from typing import Literal, Optional

from reportlab.lib.colors import black, HexColor

from .pdf_utils import (
    create_canvas_with_bleed,
    size_with_bleed_points,
    draw_centered_title,
    draw_footer_page_number,
    draw_dot_grid,
    page_margins_with_gutter,
    register_body_font,
    DEFAULT_MARGIN,
)

PageStyle = Literal["lined", "dotted", "blank"]


def _draw_lined_content(canvas, left: float, right: float, top: float, bottom: float, line_spacing: float = 24.0):
    y = bottom
    canvas.setLineWidth(0.5)
    while y < (top):
        canvas.setStrokeColor(black)
        canvas.line(left, y, right, y)
        y += line_spacing


def _draw_dotted_content(canvas, left: float, right: float, top: float, bottom: float, spacing: float = 14.4):
    canvas.saveState()
    canvas.translate(left, bottom)
    draw_dot_grid(canvas, right - left, top - bottom, 0, spacing=spacing, radius=0.8, gray=0.75)
    canvas.restoreState()


def render_notebook_pdf(
    title: str,
    pages: int,
    style: PageStyle,
    filename: str,
    trim_size: str = "6x9",
    with_bleed: bool = False,
    body_font_path: Optional[str] = None,
):
    canvas = create_canvas_with_bleed(filename, trim_size, with_bleed)
    page_width, page_height = size_with_bleed_points(trim_size, with_bleed)
    base_margin_in = DEFAULT_MARGIN / 72.0

    body_font = register_body_font(body_font_path) or "Helvetica"

    canvas.setFillColor(HexColor("#f2f2f2"))
    canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    canvas.setFillColor(black)
    draw_centered_title(canvas, page_width, page_height, title, y_ratio=0.7, font_size=40)
    canvas.setFont(body_font, 16)
    subtitle = "Notebook / Journal"
    tw = canvas.stringWidth(subtitle, body_font, 16)
    canvas.drawString((page_width - tw) / 2, page_height * 0.65, subtitle)
    canvas.showPage()

    for i in range(1, pages + 1):
        left, right, top, bottom = page_margins_with_gutter(base_margin_in, i, pages)
        # Account for bleed: content box stays the same since page is already expanded
        if style == "dotted":
            _draw_dotted_content(canvas, left, page_width - right, page_height - top, bottom)
        elif style == "blank":
            pass
        else:
            _draw_lined_content(canvas, left, page_width - right, page_height - top, bottom)
        draw_footer_page_number(canvas, page_width, DEFAULT_MARGIN, i)
        canvas.showPage()
    canvas.save()