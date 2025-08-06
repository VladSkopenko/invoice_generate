from reportlab.pdfgen import canvas
from impoved_code.config.settings import InvoiceSettings


class FooterRenderer:
    """Renderer for footer"""
    
    def __init__(self, settings: InvoiceSettings):
        self.settings = settings

    def draw_footer(self, canvas_obj: canvas.Canvas, width: float):
        """Draw footer"""
        table_width, table_center_x = self.settings.get_table_layout()

        footer_line_start = table_center_x
        footer_line_end = table_center_x + table_width

        canvas_obj.line(
            footer_line_start, self.settings.MARGIN_BOTTOM, footer_line_end, self.settings.MARGIN_BOTTOM
        )

        # Footer text
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_FOOTER)
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)
        canvas_obj.drawCentredString(width / 2, self.settings.MARGIN_BOTTOM - 20, self.settings.FOOTER_TEXT)

    def draw_payment_communication(self, canvas_obj: canvas.Canvas, invoice_number: str, totals_end_y: float):
        """Draw payment purpose"""
        _, table_center_x = self.settings.get_table_layout()

        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.drawString(
            table_center_x, totals_end_y - self.settings.SPACING_LARGE, "Призначення платежу: "
        )
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)
        canvas_obj.drawString(
            table_center_x + 135, totals_end_y - self.settings.SPACING_LARGE, invoice_number
        ) 