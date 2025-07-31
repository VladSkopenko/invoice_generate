from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from typing import List
from ...config.settings import InvoiceSettings
from ...models.invoice_data import LineItem


class ItemsTableRenderer:
    """Рендерер таблицы товаров"""
    
    def __init__(self, settings: InvoiceSettings):
        self.settings = settings

    def draw(self, canvas_obj: canvas.Canvas, line_items: List[LineItem], vat_rate: float, currency: str, start_y: float):
        """
        Отрисовка таблицы товаров
        
        Args:
            canvas_obj: Canvas для отрисовки
            line_items: Список товарных позиций
            vat_rate: Ставка НДС
            currency: Символ валюты
            start_y: Начальная Y-координата
            
        Returns:
            tuple: (subtotal, total_vat, new_y)
        """
        subtotal = 0
        table_data = [self.settings.TABLE_HEADERS]

        # Стиль для описания товара
        description_style = ParagraphStyle(
            name="DescriptionStyle",
            fontName=self.settings.NORMAL_FONT,
            fontSize=self.settings.FONT_SIZE_SMALL,
            leading=12,
            wordWrap="CJK",
        )

        # Добавление товарных позиций в таблицу
        for item in line_items:
            amount = item.get_amount()
            subtotal += amount

            description_paragraph = Paragraph(item.description, description_style)

            table_data.append(
                [
                    description_paragraph,
                    f"{item.quantity:.2f}",
                    f"{item.unit_price:.2f}",
                    f"{vat_rate}%",
                    f"{currency} {amount:.2f}",
                ]
            )

        # Создание и стилизация таблицы
        table = Table(table_data, colWidths=self.settings.TABLE_COL_WIDTHS)
        table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (0, 0), "LEFT"),
                    ("ALIGN", (1, 0), (-1, 0), "RIGHT"),
                    ("ALIGN", (0, 1), (0, -1), "RIGHT"),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, 0), self.settings.BOLD_FONT),
                    ("FONTSIZE", (0, 0), (-1, 0), self.settings.FONT_SIZE_NORMAL),
                    ("FONTNAME", (0, 1), (-1, -1), self.settings.NORMAL_FONT),
                    ("FONTSIZE", (0, 1), (-1, -1), self.settings.FONT_SIZE_SMALL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        # Расчет позиции таблицы
        table.wrapOn(canvas_obj, A4[0], A4[1])
        table_height = table._height

        base_table_y = start_y - self.settings.SECTION_TABLE_OFFSET
        table_y = base_table_y - table_height + 30

        # Отрисовка таблицы
        table_width, table_center_x = self.settings.get_table_layout()
        table.drawOn(canvas_obj, table_center_x, table_y)

        new_y = table_y - self.settings.SPACING_LARGE
        total_vat = subtotal * (vat_rate / 100)
        
        return subtotal, total_vat, new_y 