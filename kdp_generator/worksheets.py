def render_multiplication_table_pdf(filename: str, upto: int = 10, trim_size: str = "8.5x11"):
    # Walidacja parametrów
    if upto < 1 or upto > 20:
        raise ValueError("Parameter 'upto' must be between 1 and 20.")

    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    # Rysowanie tytułu i ręczne ustawienie content_top_y
    draw_page_title(canvas, page_width, page_height, f"Multiplication Table up to {upto}")
    content_top_y = page_height - margin - 40  # Zakładamy, że tytuł zajmuje ~40 punktów

    # Obliczanie siatki
    grid_w = page_width - 2 * margin
    grid_h = content_top_y - margin - 40  # Dodatkowy odstęp na dole
    cell = min(grid_w / (upto + 1), grid_h / (upto + 1))
    total_w = cell * (upto + 1)
    total_h = cell * (upto + 1)

    # Centrowanie siatki
    x0 = (page_width - total_w) / 2
    y0 = margin + (content_top_y - margin - total_h) / 2

    # Rysowanie siatki
    canvas.setStrokeColor(black)
    for i in range(upto + 2):
        # Linie poziome
        y = y0 + i * cell
        canvas.setLineWidth(2 if i in (0, 1, upto + 1) else 0.5)
        canvas.line(x0, y, x0 + total_w, y)

        # Linie pionowe
        x = x0 + i * cell
        canvas.setLineWidth(2 if i in (0, 1, upto + 1) else 0.5)
        canvas.line(x, y0, x, y0 + total_h)

    # Wypełnianie komórek
    font_size = min(12, cell * 0.5)
    canvas.setFont("Helvetica", font_size)
    for r_idx in range(1, upto + 1):
        for c_idx in range(1, upto + 1):
            # Nagłówki
            if r_idx == 1:
                canvas.setFont("Helvetica-Bold", font_size + 2)
                cx_header = x0 + (c_idx + 0.5) * cell
                cy_header = y0 + (upto + 0.5) * cell
                canvas.drawCentredString(cx_header, cy_header - font_size / 2, str(c_idx))

            if c_idx == 1:
                canvas.setFont("Helvetica-Bold", font_size + 2)
                cx_header = x0 + 0.5 * cell
                cy_header = y0 + (upto - r_idx + 0.5) * cell
                canvas.drawCentredString(cx_header, cy_header - font_size / 2, str(r_idx))

            # Treść komórki
            canvas.setFont("Helvetica", font_size)
            text = f"{r_idx} × {c_idx} = ____"
            cx = x0 + (c_idx + 0.5) * cell
            cy = y0 + (upto - r_idx + 0.5) * cell
            canvas.drawCentredString(cx, cy - font_size / 2, text)

    draw_footer_page_number(canvas, page_width, margin, 1)
    canvas.showPage()
    canvas.save()
