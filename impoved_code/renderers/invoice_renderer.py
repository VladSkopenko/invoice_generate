from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import List

from impoved_code.config.settings import InvoiceSettings
from impoved_code.config.currencies import CurrencyMapping
from impoved_code.models.invoice_data import InvoiceData, LineItem
from impoved_code.services.font_manager import FontManager
from impoved_code.renderers.components.header import HeaderRenderer
from impoved_code.renderers.components.company_info import CompanyInfoRenderer
from impoved_code.renderers.components.items_table import ItemsTableRenderer
from impoved_code.renderers.components.totals import TotalsRenderer
from impoved_code.renderers.components.footer import FooterRenderer


class InvoiceRenderer:

    
    def __init__(self):
        self.settings = InvoiceSettings()
        self.font_manager = FontManager()
        
        # Rendering components
        self.header_renderer = HeaderRenderer(self.settings)
        self.company_renderer = CompanyInfoRenderer(self.settings)
        self.table_renderer = ItemsTableRenderer(self.settings)
        self.totals_renderer = TotalsRenderer(self.settings)
        self.footer_renderer = FooterRenderer(self.settings)

    def render(self, invoice_data: InvoiceData, filename: str) -> None:
        """
        Render invoice
        
        Args:
            invoice_data: Invoice data
            filename: Filename for saving
        """
        self.font_manager.register_times_fonts()

        canvas_obj = canvas.Canvas(filename, pagesize=self.settings.PAGE_SIZE)
        width, height = self.settings.PAGE_WIDTH, self.settings.PAGE_HEIGHT

        currency_symbol = CurrencyMapping.get_symbol(invoice_data.currency)
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

        # Save file
        canvas_obj.save()

    def _draw_invoice_header(self, canvas_obj: canvas.Canvas, invoice_number: str, start_y: float):
        """Draw invoice header"""
        _, table_center_x = self.settings.get_table_layout()

        canvas_obj.setFont(self.settings.TITLE_FONT, self.settings.FONT_SIZE_HEADER)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_INVOICE_OFFSET,
            f"Рахунок-фактура {invoice_number}",
        )

    def _draw_invoice_details(self, canvas_obj: canvas.Canvas, invoice_date, due_date, source: str, start_y: float):
        """Draw invoice details"""
        table_width, table_center_x = self.settings.get_table_layout()

        canvas_obj.setFillColor(self.settings.TEXT_COLOR)

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

        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        
        # Convert date objects to strings
        invoice_date_str = invoice_date.strftime("%d.%m.%Y") if hasattr(invoice_date, 'strftime') else str(invoice_date)
        due_date_str = due_date.strftime("%d.%m.%Y") if hasattr(due_date, 'strftime') else str(due_date)
        
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_DETAILS_OFFSET - self.settings.SPACING_LARGE,
            invoice_date_str,
        )
        canvas_obj.drawString(
            table_center_x + table_width / 3,
            start_y - self.settings.SECTION_DETAILS_OFFSET - self.settings.SPACING_LARGE,
            due_date_str,
        )
        canvas_obj.drawString(
            table_center_x + table_width * 2 / 3,
            start_y - self.settings.SECTION_DETAILS_OFFSET - self.settings.SPACING_LARGE,
            source,
        ) 


if __name__ == "__main__":
    renderer = InvoiceRenderer()
    renderer.render(InvoiceData.model_validate_json(open("invoice_data.json").read()), "invoice.pdf")