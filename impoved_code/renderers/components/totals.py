from reportlab.pdfgen import canvas
from ...config.settings import InvoiceSettings


class TotalsRenderer:
    """Рендерер итогов"""
    
    def __init__(self, settings: InvoiceSettings):
        self.settings = settings

    def draw(self, canvas_obj: canvas.Canvas, subtotal: float, total_vat: float, vat_rate: float, currency: str, table_end_y: float) -> float:
        """
        Отрисовка итогов
        
        Args:
            canvas_obj: Canvas для отрисовки
            subtotal: Сумма без НДС
            total_vat: Сумма НДС
            vat_rate: Ставка НДС
            currency: Символ валюты
            table_end_y: Y-координата конца таблицы
            
        Returns:
            float: Y-координата для следующего элемента
        """
        total = subtotal + total_vat
        totals_y = table_end_y

        table_width, table_center_x = self.settings.get_table_layout()

        totals_start_x = table_center_x + self.settings.TABLE_COL_WIDTHS[0]
        totals_end_x = table_center_x + table_width

        # Линия над итогами
        canvas_obj.line(totals_start_x, totals_y, totals_end_x, totals_y)

        # Сумма без НДС
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(
            totals_start_x, totals_y - self.settings.SPACING_LARGE, f"Сума без ПДВ:"
        )
        
        # НДС
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)
        canvas_obj.drawString(
            totals_start_x, totals_y - self.settings.SPACING_LARGE * 2, f"ПДВ {vat_rate}%:"
        )

        # Линия перед итогом
        canvas_obj.line(
            totals_start_x,
            totals_y - self.settings.SPACING_LARGE * 2.5,
            totals_end_x,
            totals_y - self.settings.SPACING_LARGE * 2.5,
        )

        # Итого
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_SUBHEADER)
        canvas_obj.drawString(
            totals_start_x, totals_y - self.settings.SPACING_LARGE * 3.5, "Всього:"
        )

        # Суммы справа
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