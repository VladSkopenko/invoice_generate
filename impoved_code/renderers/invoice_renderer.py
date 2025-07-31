from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import List

from ..config.settings import InvoiceSettings
from ..config.currencies import CurrencyMapping
from ..models.invoice_data import InvoiceData, LineItem
from ..services.font_manager import FontManager
from .components.header import HeaderRenderer
from .components.company_info import CompanyInfoRenderer
from .components.items_table import ItemsTableRenderer
from .components.totals import TotalsRenderer
from .components.footer import FooterRenderer


class InvoiceRenderer:
    """Основной рендерер счета-фактуры"""
    
    def __init__(self):
        self.settings = InvoiceSettings()
        self.font_manager = FontManager()
        
        # Компоненты рендеринга
        self.header_renderer = HeaderRenderer(self.settings)
        self.company_renderer = CompanyInfoRenderer(self.settings)
        self.table_renderer = ItemsTableRenderer(self.settings)
        self.totals_renderer = TotalsRenderer(self.settings)
        self.footer_renderer = FooterRenderer(self.settings)

    def render(self, invoice_data: InvoiceData, filename: str) -> None:
        """
        Отрисовка счета-фактуры
        
        Args:
            invoice_data: Данные счета
            filename: Имя файла для сохранения
        """
        # Валидация данных
        errors = self.validation_service.validate_invoice_data(invoice_data)
        if errors:
            raise ValueError(f"Ошибки валидации: {', '.join(errors)}")

        # Регистрация шрифтов
        self.font_manager.register_times_fonts()

        # Создание canvas
        canvas_obj = canvas.Canvas(filename, pagesize=self.settings.PAGE_SIZE)
        width, height = self.settings.PAGE_WIDTH, self.settings.PAGE_HEIGHT

        # Получение символа валюты
        currency_symbol = CurrencyMapping.get_symbol(invoice_data.currency)

        # Отрисовка компонентов
        company_start_y = self.header_renderer.draw_logo(canvas_obj, height)
        
        self.company_renderer.draw_seller(canvas_obj, invoice_data.seller, company_start_y)
        self.company_renderer.draw_bank_details(canvas_obj, invoice_data.bank, company_start_y)
        self.company_renderer.draw_buyer(canvas_obj, invoice_data.buyer, company_start_y)
        
        self._draw_invoice_header(canvas_obj, invoice_data.invoice_number, company_start_y)
        self._draw_invoice_details(canvas_obj, invoice_data.invoice_date, invoice_data.due_date, invoice_data.source, company_start_y)
        
        subtotal, total_vat, table_end_y = self.table_renderer.draw(
            canvas_obj, invoice_data.line_items, invoice_data.vat_rate, currency_symbol, company_start_y
        )
        
        totals_end_y = self.totals_renderer.draw(
            canvas_obj, subtotal, total_vat, invoice_data.vat_rate, currency_symbol, table_end_y
        )
        
        self.footer_renderer.draw_payment_communication(canvas_obj, invoice_data.invoice_number, totals_end_y)
        self.footer_renderer.draw_footer(canvas_obj, width)

        # Сохранение файла
        canvas_obj.save()

    def _draw_invoice_header(self, canvas_obj: canvas.Canvas, invoice_number: str, start_y: float):
        """Отрисовка заголовка счета"""
        table_width, table_center_x = self.settings.get_table_layout()

        canvas_obj.setFont(self.settings.TITLE_FONT, self.settings.FONT_SIZE_HEADER)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_INVOICE_OFFSET,
            f"Рахунок-фактура {invoice_number}",
        )

    def _draw_invoice_details(self, canvas_obj: canvas.Canvas, invoice_date: str, due_date: str, source: str, start_y: float):
        """Отрисовка деталей счета"""
        table_width, table_center_x = self.settings.get_table_layout()

        canvas_obj.setFillColor(self.settings.TEXT_COLOR)

        # Заголовки
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.drawString(
            table_center_x, start_y - self.settings.SECTION_DETAILS_OFFSET, "Дата:"
        )
        canvas_obj.drawString(
            table_center_x + table_width / 3,
            start_y - self.settings.SECTION_DETAILS_OFFSET,
            "Термін оплати:",
        )
        canvas_obj.drawString(
            table_center_x + table_width * 2 / 3,
            start_y - self.settings.SECTION_DETAILS_OFFSET,
            "Джерело:",
        )

        # Значения
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_DETAILS_OFFSET - self.settings.SPACING_LARGE,
            invoice_date,
        )
        canvas_obj.drawString(
            table_center_x + table_width / 3,
            start_y - self.settings.SECTION_DETAILS_OFFSET - self.settings.SPACING_LARGE,
            due_date,
        )
        canvas_obj.drawString(
            table_center_x + table_width * 2 / 3,
            start_y - self.settings.SECTION_DETAILS_OFFSET - self.settings.SPACING_LARGE,
            source,
        ) 