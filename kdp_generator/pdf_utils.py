from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, white, HexColor
from typing import Tuple

KDP_SIZES_INCHES = {
    "6x9": (6.0, 9.0),
    "8.5x11": (8.5, 11.0),
    "8x10": (8.0, 10.0),
    "7x10": (7.0, 10.0),
}


def size_to_points(trim_size: str) -> Tuple[float, float]:
    if trim_size not in KDP_SIZES_INCHES:
        raise ValueError(f"Unsupported trim size '{trim_size}'. Supported: {sorted(KDP_SIZES_INCHES.keys())}")
    w_in, h_in = KDP_SIZES_INCHES[trim_size]
    return w_in * inch, h_in * inch


def create_canvas(filename: str, trim_size: str) -> Canvas:
    width, height = size_to_points(trim_size)
    return Canvas(filename, pagesize=(width, height))


def draw_centered_title(canvas: Canvas, page_width: float, page_height: float, title: str, y_ratio: float = 0.8, font_name: str = "Helvetica-Bold", font_size: int = 36):
    canvas.setFillColor(black)
    canvas.setFont(font_name, font_size)
    text_width = canvas.stringWidth(title, font_name, font_size)
    canvas.drawString((page_width - text_width) / 2, page_height * y_ratio, title)


def draw_footer_page_number(canvas: Canvas, page_width: float, margin: float, page_number: int, font_name: str = "Helvetica", font_size: int = 10):
    canvas.setFont(font_name, font_size)
    canvas.setFillColor(black)
    text = str(page_number)
    text_width = canvas.stringWidth(text, font_name, font_size)
    canvas.drawString(page_width - margin - text_width, margin * 0.6, text)