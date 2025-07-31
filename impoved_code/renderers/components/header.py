from reportlab.pdfgen import canvas
from ...config.settings import InvoiceSettings


class HeaderRenderer:
    """Renderer for header and logo"""
    
    def __init__(self, settings: InvoiceSettings):
        self.settings = settings

    def draw_logo(self, canvas_obj: canvas.Canvas, height: float) -> float:
        """Draw logo and header"""
        table_width, table_center_x = self.settings.get_table_layout()

        # Draw logo
        canvas_obj.setFont(self.settings.TITLE_FONT, self.settings.FONT_SIZE_TITLE)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(table_center_x, height - self.settings.MARGIN_TOP, self.settings.LOGO_TEXT)

        # Draw line under logo
        top_line_start = table_center_x
        top_line_end = table_center_x + table_width

        canvas_obj.line(
            top_line_start,
            height - self.settings.MARGIN_TOP - 20,
            top_line_end,
            height - self.settings.MARGIN_TOP - 20,
        )
        
        return height - self.settings.SECTION_LOGO_OFFSET 