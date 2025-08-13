from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, white, HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import Tuple, Optional

KDP_SIZES_INCHES = {
    "6x9": (6.0, 9.0),
    "8.5x11": (8.5, 11.0),
    "8x10": (8.0, 10.0),
    "7x10": (7.0, 10.0),
}

DEFAULT_MARGIN = 0.75 * 72
DEFAULT_BLEED_INCH = 0.125


def size_to_points(trim_size: str) -> Tuple[float, float]:
    if trim_size not in KDP_SIZES_INCHES:
        raise ValueError(f"Unsupported trim size '{trim_size}'. Supported: {sorted(KDP_SIZES_INCHES.keys())}")
    w_in, h_in = KDP_SIZES_INCHES[trim_size]
    return w_in * inch, h_in * inch


def size_with_bleed_points(trim_size: str, with_bleed: bool) -> Tuple[float, float]:
    w_pt, h_pt = size_to_points(trim_size)
    if not with_bleed:
        return w_pt, h_pt
    bleed_pt = DEFAULT_BLEED_INCH * inch
    return w_pt + 2 * bleed_pt, h_pt + 2 * bleed_pt


def create_canvas(filename: str, trim_size: str) -> Canvas:
    width, height = size_to_points(trim_size)
    return Canvas(filename, pagesize=(width, height))


def create_canvas_with_bleed(filename: str, trim_size: str, with_bleed: bool) -> Canvas:
    width, height = size_with_bleed_points(trim_size, with_bleed)
    return Canvas(filename, pagesize=(width, height))


def compute_gutter_inches(page_count: int) -> float:
    if page_count <= 150:
        return 0.375
    if page_count <= 300:
        return 0.5
    return 0.625


def page_margins_with_gutter(base_margin_inch: float, page_index_one_based: int, page_count: int) -> Tuple[float, float, float, float]:
    """Return (left, right, top, bottom) in points, with gutter on inner side.
    page_index_one_based: 1..N; odd pages are right-hand (inner on left), even pages left-hand (inner on right)
    """
    gutter_in = compute_gutter_inches(page_count)
    left_in = right_in = base_margin_inch
    if page_index_one_based % 2 == 1:
        # right-hand page: inner is left
        left_in += gutter_in
    else:
        # left-hand page: inner is right
        right_in += gutter_in
    top_in = bottom_in = base_margin_inch
    return left_in * inch, right_in * inch, top_in * inch, bottom_in * inch


def draw_centered_title(canvas: Canvas, page_width: float, page_height: float, title: str, y_ratio: float = 0.8, font_name: str = "Helvetica-Bold", font_size: int = 36):
    canvas.setFillColor(black)
    canvas.setFont(font_name, font_size)
    text_width = canvas.stringWidth(title, font_name, font_size)
    canvas.drawString((page_width - text_width) / 2, page_height * y_ratio, title)


def draw_page_title(canvas: Canvas, page_width: float, page_height: float, title: str, font_name: str = "Helvetica-Bold", font_size: int = 18):
    canvas.setFillColor(black)
    canvas.setFont(font_name, font_size)
    tw = canvas.stringWidth(title, font_name, font_size)
    canvas.drawString((page_width - tw) / 2, page_height - DEFAULT_MARGIN + 8, title)


def draw_footer_page_number(canvas: Canvas, page_width: float, margin: float, page_number: int, font_name: str = "Helvetica", font_size: int = 10):
    canvas.setFont(font_name, font_size)
    canvas.setFillColor(black)
    text = str(page_number)
    text_width = canvas.stringWidth(text, font_name, font_size)
    canvas.drawString(page_width - margin - text_width, margin * 0.6, text)


def draw_dot_grid(canvas: Canvas, page_width: float, page_height: float, margin: float, spacing: float = 14.4, radius: float = 0.8, gray: float = 0.75):
    canvas.setStrokeColor(Color(gray, gray, gray))
    x = margin
    y = margin
    while y <= page_height - margin:
        x = margin
        while x <= page_width - margin:
            canvas.circle(x, y, radius, stroke=1, fill=0)
            x += spacing
        y += spacing


def register_body_font(font_path: Optional[str], name: str = 'BodyTTF') -> Optional[str]:
    if not font_path:
        return None
    try:
        pdfmetrics.registerFont(TTFont(name, font_path))
        return name
    except Exception:
        return None