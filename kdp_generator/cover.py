from typing import Optional
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, HexColor
from reportlab.lib.units import inch
from .pdf_utils import create_canvas, size_to_points

PAPER_THICKNESS_INCH = {
    'bw_55': 0.002252,
    'color_60': 0.0026,
}

BLEED_INCH = 0.125
SAFE_INCH = 0.25
BARCODE_W_IN = 2.0
BARCODE_H_IN = 1.2


def calc_spine_width_inches(page_count: int, stock: str = 'bw_55') -> float:
    t = PAPER_THICKNESS_INCH.get(stock, PAPER_THICKNESS_INCH['bw_55'])
    return page_count * t


def register_font_if_needed(font_path: Optional[str], font_name: str = 'CustomCover') -> Optional[str]:
    if font_path:
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            return font_name
        except Exception:
            return None
    return None


def render_kdp_cover_pdf(
    filename: str,
    trim_size: str = '6x9',
    page_count: int = 120,
    stock: str = 'bw_55',
    with_bleed: bool = True,
    title: str = 'My Book',
    subtitle: Optional[str] = None,
    author: Optional[str] = None,
    bg_color: str = '#ffffff',
    accent_color: str = '#000000',
    font_path: Optional[str] = None,
    show_guides: bool = False,
):
    w_in, h_in = (s/72.0 for s in size_to_points(trim_size))
    bleed = BLEED_INCH if with_bleed else 0.0
    spine_in = calc_spine_width_inches(page_count, stock)

    cover_w_in = w_in * 2 + spine_in + 2 * bleed
    cover_h_in = h_in + 2 * bleed

    from reportlab.lib.units import inch
    canvas = create_canvas(filename, trim_size)
    canvas.setPageSize((cover_w_in * inch, cover_h_in * inch))

    bg = HexColor(bg_color)
    accent = HexColor(accent_color)

    canvas.setFillColor(bg)
    canvas.rect(0, 0, cover_w_in * inch, cover_h_in * inch, fill=1, stroke=0)

    # Guides: safe areas and barcode box
    if show_guides:
        canvas.setStrokeColor(HexColor('#cccccc'))
        # Spine area
        canvas.rect((bleed + w_in) * inch, 0, spine_in * inch, cover_h_in * inch, stroke=1, fill=0)
        # Safe areas front/back
        safe = SAFE_INCH
        # Back safe
        canvas.rect(bleed * inch + safe * inch, bleed * inch + safe * inch, (w_in - 2*safe) * inch, (h_in - 2*safe) * inch, stroke=1, fill=0)
        # Front safe
        canvas.rect((bleed + w_in + spine_in + safe) * inch, (bleed + safe) * inch, (w_in - 2*safe) * inch, (h_in - 2*safe) * inch, stroke=1, fill=0)
        # Barcode box on back bottom-right
        canvas.setStrokeColor(HexColor('#999999'))
        canvas.rect((bleed + w_in - BARCODE_W_IN - 0.25) * inch, (bleed + 0.25) * inch, BARCODE_W_IN * inch, BARCODE_H_IN * inch, stroke=1, fill=0)

    chosen_font = register_font_if_needed(font_path) or 'Helvetica-Bold'
    chosen_font_sub = register_font_if_needed(font_path) or 'Helvetica'

    canvas.setFillColor(accent)
    # Front cover text
    front_x = (w_in + spine_in + bleed) * inch
    front_y = bleed * inch
    front_w = w_in * inch
    front_h = h_in * inch

    canvas.setFont(chosen_font, 48)
    tw = canvas.stringWidth(title, chosen_font, 48)
    canvas.drawString(front_x + (front_w - tw) / 2, front_y + front_h * 0.6, title)
    if subtitle:
        canvas.setFont(chosen_font_sub, 18)
        stw = canvas.stringWidth(subtitle, chosen_font_sub, 18)
        canvas.drawString(front_x + (front_w - stw) / 2, front_y + front_h * 0.55, subtitle)
    if author:
        canvas.setFont(chosen_font_sub, 16)
        atw = canvas.stringWidth(author, chosen_font_sub, 16)
        canvas.drawString(front_x + (front_w - atw) / 2, front_y + front_h * 0.1, author)

    # Spine text vertical (reading bottom-to-top)
    canvas.saveState()
    cx = (w_in + bleed + spine_in/2) * inch
    cy = cover_h_in * inch / 2
    canvas.translate(cx, cy)
    canvas.rotate(90)
    canvas.setFont(chosen_font_sub, 16)
    st = title[:60]
    stw = canvas.stringWidth(st, chosen_font_sub, 16)
    canvas.drawString(-stw / 2, -8, st)
    canvas.restoreState()

    canvas.showPage()
    canvas.save()