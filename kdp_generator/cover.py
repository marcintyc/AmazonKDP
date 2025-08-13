from typing import Optional
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, HexColor
from .pdf_utils import create_canvas, size_to_points

PAPER_THICKNESS_INCH = {
    'bw_55': 0.002252,  # B&W 55lb
    'color_60': 0.0026, # Color 60lb (approx)
}

BLEED_INCH = 0.125


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
):
    w_in, h_in = (s/72.0 for s in size_to_points(trim_size))
    bleed = BLEED_INCH if with_bleed else 0.0
    spine_in = calc_spine_width_inches(page_count, stock)

    cover_w_in = w_in * 2 + spine_in + 2 * bleed
    cover_h_in = h_in + 2 * bleed

    from reportlab.lib.units import inch
    canvas = create_canvas(filename, trim_size)  # temporary size replaced below
    canvas.setPageSize((cover_w_in * inch, cover_h_in * inch))

    bg = HexColor(bg_color)
    accent = HexColor(accent_color)

    canvas.setFillColor(bg)
    canvas.rect(0, 0, cover_w_in * inch, cover_h_in * inch, fill=1, stroke=0)

    chosen_font = register_font_if_needed(font_path) or 'Helvetica-Bold'
    chosen_font_sub = register_font_if_needed(font_path) or 'Helvetica'

    canvas.setFillColor(accent)
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

    canvas.saveState()
    canvas.translate((w_in + bleed + spine_in/2) * inch, cover_h_in * inch / 2)
    canvas.rotate(90)
    canvas.setFont(chosen_font_sub, 16)
    st = title[:40]
    stw = canvas.stringWidth(st, chosen_font_sub, 16)
    canvas.drawString(-stw / 2, -8, st)
    canvas.restoreState()

    back_x = bleed * inch
    back_y = bleed * inch
    back_w = w_in * inch
    back_h = h_in * inch
    canvas.setStrokeColor(HexColor('#dddddd'))
    canvas.rect(back_x + back_w * 0.1, back_y + back_h * 0.2, back_w * 0.8, back_h * 0.5, stroke=1, fill=0)

    canvas.showPage()
    canvas.save()