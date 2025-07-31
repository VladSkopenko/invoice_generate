from reportlab.pdfgen import canvas
from ...config.settings import InvoiceSettings
from ...models.invoice_data import CompanyInfo, BankDetails


class CompanyInfoRenderer:
    """Рендерер информации о компаниях"""
    
    def __init__(self, settings: InvoiceSettings):
        self.settings = settings

    def draw_seller(self, canvas_obj: canvas.Canvas, company: CompanyInfo, start_y: float):
        """Отрисовка информации о продавце"""
        table_width, table_center_x = self.settings.get_table_layout()

        # Заголовок
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_SUBHEADER)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(
            table_center_x, start_y + self.settings.SECTION_COMPANY_OFFSET, "Продавець:"
        )

        # Информация о компании
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)

        canvas_obj.drawString(table_center_x, start_y - self.settings.SPACING_SMALL, company.name)
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SPACING_SMALL - self.settings.SPACING_MEDIUM,
            f"ЄДРПОУ: {company.edprou}",
        )
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SPACING_SMALL - self.settings.SPACING_MEDIUM * 2,
            company.address,
        )
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SPACING_SMALL - self.settings.SPACING_MEDIUM * 3,
            company.country,
        )

    def draw_buyer(self, canvas_obj: canvas.Canvas, company: CompanyInfo, start_y: float):
        """Отрисовка информации о покупателе"""
        table_width, table_center_x = self.settings.get_table_layout()
        buyer_x = table_center_x + table_width - 250

        # Заголовок
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_SUBHEADER)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(buyer_x, start_y + self.settings.SECTION_COMPANY_OFFSET, "Покупець:")

        # Информация о компании
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_NORMAL)
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)

        canvas_obj.drawString(buyer_x, start_y - self.settings.SPACING_SMALL, company.name)
        canvas_obj.drawString(
            buyer_x,
            start_y - self.settings.SPACING_SMALL - self.settings.SPACING_MEDIUM,
            f"ЄДРПОУ: {company.edprou}",
        )
        canvas_obj.drawString(
            buyer_x, start_y - self.settings.SPACING_SMALL - self.settings.SPACING_MEDIUM * 2, company.address
        )
        canvas_obj.drawString(
            buyer_x, start_y - self.settings.SPACING_SMALL - self.settings.SPACING_MEDIUM * 3, company.country
        )

    def draw_bank_details(self, canvas_obj: canvas.Canvas, bank: BankDetails, start_y: float):
        """Отрисовка банковских реквизитов"""
        table_width, table_center_x = self.settings.get_table_layout()

        # Заголовок
        canvas_obj.setFont(self.settings.BOLD_FONT, self.settings.FONT_SIZE_SMALL)
        canvas_obj.setFillColor(self.settings.PRIMARY_COLOR)
        canvas_obj.drawString(
            table_center_x, start_y - self.settings.SECTION_BANK_OFFSET, "Банківські реквізити:"
        )

        # Банковские реквизиты
        canvas_obj.setFont(self.settings.NORMAL_FONT, self.settings.FONT_SIZE_FOOTER)
        canvas_obj.setFillColor(self.settings.TEXT_COLOR)
        
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_BANK_OFFSET - self.settings.SPACING_LARGE,
            f"Банк: {bank.name}",
        )
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_BANK_OFFSET - self.settings.SPACING_LARGE * 2,
            f"МФО: {bank.mfo}",
        )
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_BANK_OFFSET - self.settings.SPACING_LARGE * 3,
            f"Адреса: {bank.address}",
        )
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_BANK_OFFSET - self.settings.SPACING_LARGE * 4,
            f"SWIFT: {bank.swift}",
        )
        canvas_obj.drawString(
            table_center_x,
            start_y - self.settings.SECTION_BANK_OFFSET - self.settings.SPACING_LARGE * 5,
            f"IBAN: {bank.iban}",
        ) 