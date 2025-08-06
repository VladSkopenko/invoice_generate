from reportlab.pdfgen import canvas
from decimal import Decimal
from impoved_code.config.settings import InvoiceSettings


class TotalsRenderer:
    """Renderer for totals"""
    
    def __init__(self, settings: InvoiceSettings):
        self.settings = settings

    def draw(self, canvas_obj: canvas.Canvas, subtotal: Decimal, total_vat: Decimal, vat_rate: Decimal, currency: str, table_end_y: float) -> float:
        """
        Draw totals
        
        Args:
            canvas_obj: Canvas for drawing
            subtotal: Amount without VAT
            total_vat: VAT amount
            vat_rate: VAT rate
            currency: Currency symbol
            table_end_y: Y coordinate of table end
            
        Returns:
            float: Y coordinate for next element
        """
        total = subtotal + total_vat
        totals_y = table_end_y

        table_width, table_center_x = self.settings.get_table_layout()

        totals_start_x = table_center_x + self.settings.TABLE_COL_WIDTHS[0]
        totals_end_x = table_center_x + table_width

        # Line above totals
        canvas_obj.line(totals_start_x, totals_y, totals_end_x, totals_y)

        # Amount without VAT
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(
            totals_start_x, totals_y - self.settings.SPACING_LARGE, f"Сума без ПДВ:"
        )
        
        # VAT
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)
        canvas_obj.drawString(
            totals_start_x, totals_y - self.settings.SPACING_LARGE * 2, f"ПДВ {vat_rate}%:"
        )

        # Line before total
        canvas_obj.line(
            totals_start_x,
            totals_y - self.settings.SPACING_LARGE * 2.5,
            totals_end_x,
            totals_y - self.settings.SPACING_LARGE * 2.5,
        )

        # Total
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_SUBHEADER)
        canvas_obj.drawString(
            totals_start_x, totals_y - self.settings.SPACING_LARGE * 3.5, "Всього:"
        )

        # Amounts on the right
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)
        canvas_obj.drawRightString(
            totals_end_x, totals_y - self.settings.SPACING_LARGE, f"{currency} {subtotal:.2f}"
        )
        canvas_obj.drawRightString(
            totals_end_x, totals_y - self.settings.SPACING_LARGE * 2, f"{currency} {total_vat:.2f}"
        )
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_SUBHEADER)
        canvas_obj.drawRightString(
            totals_end_x, totals_y - self.settings.SPACING_LARGE * 3.5, f"{currency} {total:.2f}"
        )

        return totals_y - self.settings.SPACING_LARGE * 4 