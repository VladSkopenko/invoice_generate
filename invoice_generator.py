from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import os


class InvoiceGenerator:
    MARGIN_LEFT = 50
    MARGIN_RIGHT = 50
    MARGIN_TOP = 30
    MARGIN_BOTTOM = 80

    FONT_SIZE_TITLE = 24
    FONT_SIZE_HEADER = 20
    FONT_SIZE_SUBHEADER = 14
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_SMALL = 11
    FONT_SIZE_FOOTER = 9

    SPACING_SMALL = 15
    SPACING_MEDIUM = 18
    SPACING_LARGE = 20
    SPACING_XLARGE = 25

    COLUMN_LEFT_X = 50
    COLUMN_RIGHT_X = 350

    TOTALS_RIGHT_X = 590

    TOTALS_START_X = 300
    TOTALS_END_X = 580

    SECTION_LOGO_OFFSET = 70
    SECTION_COMPANY_OFFSET = 5
    SECTION_BANK_OFFSET = 95
    SECTION_INVOICE_OFFSET = 275
    SECTION_DETAILS_OFFSET = 300
    SECTION_TABLE_OFFSET = 370
    SECTION_TOTALS_OFFSET = 400
    SECTION_PAYMENT_OFFSET = 520

    TABLE_HEADERS = ["Опис", "Кількість", "Ціна за одиницю", "ПДВ", "Сума"]
    TABLE_COL_WIDTHS = [250, 68, 105, 35, 65]
    TABLE_ROW_HEIGHT = 20
    TABLE_DESCRIPTION_WRAP_WIDTH = 240

    FOOTER_TEXT = "Рахунок створений платформою https://inbulk.com"
    LOGO_TEXT = "In Bulk"

    def __init__(self):
        self.fonts_registered = False
        self.register_times_fonts()

        self.title_font = "Times-Bold"
        self.normal_font = "Times"
        self.bold_font = "Times-Bold"
        self.italic_font = "Times-Italic"

        self.primary_color = colors.HexColor("#800080")
        self.text_color = colors.black
        self.white_color = colors.white

    @property
    def table_layout(self):
        table_width = sum(self.TABLE_COL_WIDTHS)
        page_center = A4[0] / 2
        table_center_x = page_center - table_width / 2
        return table_width, table_center_x

    def register_times_fonts(self):
        if self.fonts_registered:
            return

        fonts_dir = "fonts"
        font_files = {
            "Times": "TIMES.TTF",
            "Times-Bold": "TIMESBD.TTF",
            "Times-Italic": "TIMESI.TTF",
            "Times-BoldItalic": "TIMESBI.TTF",
        }

        for font_name, font_file in font_files.items():
            font_path = os.path.join(fonts_dir, font_file)
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                except:
                    pass

        self.fonts_registered = True

    def generate_invoice(
        self,
        filename: str,
        company_seller_name: str,
        company_seller_edprou: str,
        company_seller_address: str,
        company_seller_country: str,
        bank_name_seller: str,
        bank_mfo_seller: str,
        bank_address_seller: str,
        bank_swift_seller: str,
        bank_iban_seller: str,
        company_buyer_name: str,
        client_buyer_edprou: str,
        client_buyer_address: str,
        client_buyer_country: str,
        invoice_number: str,
        invoice_date: str,
        due_date: str,
        source: str,
        line_items=None,
        vat_rate=20,
    ):

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        company_start_y = self._draw_logo(canvas=c, height=height)
        self._draw_company_info_seller(
            canvas=c,
            name=company_seller_name,
            edprou=company_seller_edprou,
            address=company_seller_address,
            country=company_seller_country,
            start_y=company_start_y,
        )
        self._draw_bank_details(
            canvas=c,
            bank_name=bank_name_seller,
            bank_mfo=bank_mfo_seller,
            bank_address=bank_address_seller,
            bank_swift=bank_swift_seller,
            bank_iban=bank_iban_seller,
            start_y=company_start_y,
        )
        self._draw_company_info_buyer(
            canvas=c,
            name=company_buyer_name,
            edprou=client_buyer_edprou,
            address=client_buyer_address,
            country=client_buyer_country,
            start_y=company_start_y,
        )
        self._draw_invoice_header(canvas=c, invoice_number=invoice_number, start_y=company_start_y)
        self._draw_invoice_details(canvas=c, invoice_date=invoice_date, due_date=due_date, source=source, start_y=company_start_y)
        subtotal, total_vat, table_end_y = self._draw_items_table(
            canvas=c, line_items=line_items, vat_rate=vat_rate, start_y=company_start_y
        )
        totals_end_y = self._draw_totals(canvas=c, subtotal=subtotal, total_vat=total_vat, vat_rate=vat_rate, table_end_y=table_end_y)
        self._draw_payment_communication(canvas=c, invoice_number=invoice_number, totals_end_y=totals_end_y)
        self._draw_footer(canvas=c, width=width)

        c.save()

    def _draw_logo(self, canvas, height):
        table_width, table_center_x = self.table_layout

        canvas.setFont(self.title_font, self.FONT_SIZE_TITLE)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(table_center_x, height - self.MARGIN_TOP, self.LOGO_TEXT)

        top_line_start = table_center_x
        top_line_end = table_center_x + table_width

        canvas.line(
            top_line_start,
            height - self.MARGIN_TOP - 20,
            top_line_end,
            height - self.MARGIN_TOP - 20,
        )
        return height - self.SECTION_LOGO_OFFSET

    def _draw_company_info_seller(
        self, canvas, name, edprou, address, country, start_y
    ):
        table_width, table_center_x = self.table_layout

        canvas.setFont(self.bold_font, self.FONT_SIZE_SUBHEADER)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(
            table_center_x, start_y + self.SECTION_COMPANY_OFFSET, "Продавець:"
        )

        canvas.setFont(self.normal_font, self.FONT_SIZE_NORMAL)
        canvas.setFillColor(self.text_color)

        canvas.drawString(table_center_x, start_y - self.SPACING_SMALL, name)
        canvas.drawString(
            table_center_x,
            start_y - self.SPACING_SMALL - self.SPACING_MEDIUM,
            f"ЄДРПОУ: {edprou}",
        )
        canvas.drawString(
            table_center_x,
            start_y - self.SPACING_SMALL - self.SPACING_MEDIUM * 2,
            address,
        )
        canvas.drawString(
            table_center_x,
            start_y - self.SPACING_SMALL - self.SPACING_MEDIUM * 3,
            country,
        )

    def _draw_company_info_buyer(self, canvas, name, edprou, address, country, start_y):
        table_width, table_center_x = self.table_layout
        buyer_x = table_center_x + table_width - 250

        canvas.setFont(self.bold_font, self.FONT_SIZE_SUBHEADER)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(buyer_x, start_y + self.SECTION_COMPANY_OFFSET, "Покупець:")

        canvas.setFont(self.normal_font, self.FONT_SIZE_NORMAL)
        canvas.setFillColor(self.text_color)

        canvas.drawString(buyer_x, start_y - self.SPACING_SMALL, name)
        canvas.drawString(
            buyer_x,
            start_y - self.SPACING_SMALL - self.SPACING_MEDIUM,
            f"ЄДРПОУ: {edprou}",
        )
        canvas.drawString(
            buyer_x, start_y - self.SPACING_SMALL - self.SPACING_MEDIUM * 2, address
        )
        canvas.drawString(
            buyer_x, start_y - self.SPACING_SMALL - self.SPACING_MEDIUM * 3, country
        )

    def _draw_invoice_header(self, canvas, invoice_number, start_y):
        table_width, table_center_x = self.table_layout

        canvas.setFont(self.title_font, self.FONT_SIZE_HEADER)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(
            table_center_x,
            start_y - self.SECTION_INVOICE_OFFSET,
            f"Рахунок-фактура {invoice_number}",
        )

    def _draw_invoice_details(self, canvas, invoice_date, due_date, source, start_y):
        table_width, table_center_x = self.table_layout

        canvas.setFillColor(self.text_color)

        canvas.setFont(self.bold_font, self.FONT_SIZE_NORMAL)
        canvas.drawString(
            table_center_x, start_y - self.SECTION_DETAILS_OFFSET, "Дата:"
        )
        canvas.drawString(
            table_center_x + table_width / 3,
            start_y - self.SECTION_DETAILS_OFFSET,
            "Термін оплати:",
        )
        canvas.drawString(
            table_center_x + table_width * 2 / 3,
            start_y - self.SECTION_DETAILS_OFFSET,
            "Джерело:",
        )

        canvas.setFont(self.normal_font, self.FONT_SIZE_NORMAL)
        canvas.drawString(
            table_center_x,
            start_y - self.SECTION_DETAILS_OFFSET - self.SPACING_LARGE,
            invoice_date,
        )
        canvas.drawString(
            table_center_x + table_width / 3,
            start_y - self.SECTION_DETAILS_OFFSET - self.SPACING_LARGE,
            due_date,
        )
        canvas.drawString(
            table_center_x + table_width * 2 / 3,
            start_y - self.SECTION_DETAILS_OFFSET - self.SPACING_LARGE,
            source,
        )

    def _draw_items_table(self, canvas, line_items, vat_rate, start_y):
        subtotal = 0
        table_data = [self.TABLE_HEADERS]

        description_style = ParagraphStyle(
            name="DescriptionStyle",
            fontName=self.normal_font,
            fontSize=self.FONT_SIZE_SMALL,
            leading=12,
            wordWrap="CJK",
        )

        for item in line_items:
            quantity = item["quantity"]
            unit_price = item["unit_price"]
            amount = quantity * unit_price
            subtotal += amount

            description_paragraph = Paragraph(item["description"], description_style)

            table_data.append(
                [
                    description_paragraph,
                    f"{quantity:.2f}",
                    f"{unit_price:.2f}",
                    f"{vat_rate}%",
                    f"$ {amount:.2f}",
                ]
            )

        table = Table(table_data, colWidths=self.TABLE_COL_WIDTHS)
        table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (0, 0), "LEFT"),
                    ("ALIGN", (1, 0), (-1, 0), "RIGHT"),
                    ("ALIGN", (0, 1), (0, -1), "RIGHT"),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, 0), self.bold_font),
                    ("FONTSIZE", (0, 0), (-1, 0), self.FONT_SIZE_NORMAL),
                    ("FONTNAME", (0, 1), (-1, -1), self.normal_font),
                    ("FONTSIZE", (0, 1), (-1, -1), self.FONT_SIZE_SMALL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        table.wrapOn(canvas, A4[0], A4[1])
        table_height = table._height

        base_table_y = start_y - self.SECTION_TABLE_OFFSET
        table_y = base_table_y - table_height + 30

        table_width, table_center_x = self.table_layout
        table.drawOn(canvas, table_center_x, table_y)

        new_y = table_y - self.SPACING_LARGE

        total_vat = subtotal * (vat_rate / 100)
        return subtotal, total_vat, new_y

    def _draw_totals(self, canvas, subtotal, total_vat, vat_rate, table_end_y):
        total = subtotal + total_vat

        totals_y = table_end_y

        table_width, table_center_x = self.table_layout

        totals_start_x = table_center_x + self.TABLE_COL_WIDTHS[0]
        totals_end_x = table_center_x + table_width

        canvas.line(totals_start_x, totals_y, totals_end_x, totals_y)

        canvas.setFont(self.normal_font, self.FONT_SIZE_NORMAL)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(
            totals_start_x, totals_y - self.SPACING_LARGE, f"Сума без ПДВ:"
        )
        canvas.setFillColor(self.text_color)
        canvas.drawString(
            totals_start_x, totals_y - self.SPACING_LARGE * 2, f"ПДВ {vat_rate}%:"
        )

        canvas.line(
            totals_start_x,
            totals_y - self.SPACING_LARGE * 2.5,
            totals_end_x,
            totals_y - self.SPACING_LARGE * 2.5,
        )

        canvas.setFont(self.bold_font, self.FONT_SIZE_SUBHEADER)
        canvas.drawString(
            totals_start_x, totals_y - self.SPACING_LARGE * 3.5, "Всього:"
        )

        canvas.setFont(self.normal_font, self.FONT_SIZE_NORMAL)
        canvas.setFillColor(self.text_color)
        canvas.drawRightString(
            totals_end_x, totals_y - self.SPACING_LARGE, f"$ {subtotal:.2f}"
        )
        canvas.drawRightString(
            totals_end_x, totals_y - self.SPACING_LARGE * 2, f"$ {total_vat:.2f}"
        )
        canvas.setFont(self.bold_font, self.FONT_SIZE_SUBHEADER)
        canvas.drawRightString(
            totals_end_x, totals_y - self.SPACING_LARGE * 3.5, f"$ {total:.2f}"
        )

        return totals_y - self.SPACING_LARGE * 4

    def _draw_payment_communication(self, canvas, invoice_number, totals_end_y):
        table_width, table_center_x = self.table_layout

        canvas.setFont(self.normal_font, self.FONT_SIZE_NORMAL)
        canvas.drawString(
            table_center_x, totals_end_y - self.SPACING_LARGE, "Призначення платежу: "
        )
        canvas.setFont(self.bold_font, self.FONT_SIZE_NORMAL)
        canvas.setFillColor(self.text_color)
        canvas.drawString(
            table_center_x + 135, totals_end_y - self.SPACING_LARGE, invoice_number
        )

    def _draw_bank_details(
        self, canvas, bank_name, bank_mfo, bank_address, bank_swift, bank_iban, start_y
    ):
        table_width, table_center_x = self.table_layout

        canvas.setFont(self.bold_font, self.FONT_SIZE_SMALL)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(
            table_center_x, start_y - self.SECTION_BANK_OFFSET, "Банківські реквізити:"
        )

        canvas.setFont(self.normal_font, self.FONT_SIZE_FOOTER)
        canvas.setFillColor(self.text_color)
        canvas.drawString(
            table_center_x,
            start_y - self.SECTION_BANK_OFFSET - self.SPACING_LARGE,
            f"Банк: {bank_name}",
        )
        canvas.drawString(
            table_center_x,
            start_y - self.SECTION_BANK_OFFSET - self.SPACING_LARGE * 2,
            f"МФО: {bank_mfo}",
        )
        canvas.drawString(
            table_center_x,
            start_y - self.SECTION_BANK_OFFSET - self.SPACING_LARGE * 3,
            f"Адреса: {bank_address}",
        )
        canvas.drawString(
            table_center_x,
            start_y - self.SECTION_BANK_OFFSET - self.SPACING_LARGE * 4,
            f"SWIFT: {bank_swift}",
        )
        canvas.drawString(
            table_center_x,
            start_y - self.SECTION_BANK_OFFSET - self.SPACING_LARGE * 5,
            f"IBAN: {bank_iban}",
        )

    def _draw_footer(self, canvas, width):
        table_width, table_center_x = self.table_layout

        footer_line_start = table_center_x
        footer_line_end = table_center_x + table_width

        canvas.line(
            footer_line_start, self.MARGIN_BOTTOM, footer_line_end, self.MARGIN_BOTTOM
        )

        canvas.setFont(self.normal_font, self.FONT_SIZE_FOOTER)
        canvas.setFillColor(self.text_color)
        canvas.drawCentredString(width / 2, self.MARGIN_BOTTOM - 20, self.FOOTER_TEXT)


if __name__ == "__main__":
    generator = InvoiceGenerator()

    generator.generate_invoice(
        filename="invoice.pdf",
        company_seller_name="ТОВ 'Технології Майбутнього'",
        company_seller_edprou="12345678",
        company_seller_address="м. Київ, вул. Велика Васильківська, 100",
        company_seller_country="Україна",
        bank_name_seller="ПриватБанк",
        bank_mfo_seller="305299",
        bank_address_seller="м. Дніпро, вул. Набережна Перемоги, 50",
        bank_swift_seller="PBANUA2X",
        bank_iban_seller="UA123456789012345678901234567",
        company_buyer_name="ТОВ 'Інноваційні Рішення'",
        client_buyer_edprou="87654321",
        client_buyer_address="м. Львів, вул. Свободи, 15",
        client_buyer_country="Україна",
        invoice_number="РФ/2024/00001",
        invoice_date="15.01.2024",
        due_date="20.01.2024",
        source="S00001",
        line_items=[
            {
                "description": "Дуже довгий опис товару з багатьма словами для тестування автоматичного переносу тексту в таблиці рахунку-фактури",
                "quantity": 0,
                "unit_price": 0,
            },
            {
                "description": "Передоплата 10% після завантаження автомобіля",
                "quantity": 1,
                "unit_price": 800,
            },
            {
                "description": "Оплата 30% при розвантаженні автомобіля",
                "quantity": 1,
                "unit_price": 3600,
            },
            {
                "description": "Оплата 60% після отримання товару",
                "quantity": 1,
                "unit_price": 7200,
            },
        ],
        vat_rate=20,
    )
