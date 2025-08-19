# Перенесено
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


class InvoiceSettings:
    # Margins
    MARGIN_LEFT = 50
    MARGIN_RIGHT = 50
    MARGIN_TOP = 30
    MARGIN_BOTTOM = 80

    # Font sizes
    FONT_SIZE_TITLE = 24
    FONT_SIZE_HEADER = 20
    FONT_SIZE_SUBHEADER = 14
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_SMALL = 11
    FONT_SIZE_FOOTER = 9

    # Spacing
    SPACING_SMALL = 15
    SPACING_MEDIUM = 18
    SPACING_LARGE = 20
    SPACING_XLARGE = 25

    # Column positions
    COLUMN_LEFT_X = 50
    COLUMN_RIGHT_X = 350
    TOTALS_RIGHT_X = 590
    TOTALS_START_X = 300
    TOTALS_END_X = 580

    # Section offsets
    SECTION_LOGO_OFFSET = 70
    SECTION_COMPANY_OFFSET = 5
    SECTION_BANK_OFFSET = 95
    SECTION_INVOICE_OFFSET = 275
    SECTION_DETAILS_OFFSET = 300
    SECTION_TABLE_OFFSET = 370
    SECTION_TOTALS_OFFSET = 400
    SECTION_PAYMENT_OFFSET = 520

    # Table settings
    TABLE_HEADERS = ["Опис", "Кількість", "Ціна за одиницю", "ПДВ", "Сума"]
    TABLE_COL_WIDTHS = [250, 68, 105, 35, 65]
    TABLE_ROW_HEIGHT = 20
    TABLE_DESCRIPTION_WRAP_WIDTH = 240

    # Text constants
    FOOTER_TEXT = "Рахунок створений платформою https://inbulk.com"
    LOGO_TEXT = "In Bulk"

    # Colors
    PRIMARY_COLOR = colors.HexColor("#800080")
    TEXT_COLOR = colors.black
    WHITE_COLOR = colors.white

    # Fonts
    TITLE_FONT = "Times-Bold"
    NORMAL_FONT = "Times"
    BOLD_FONT = "Times-Bold"
    ITALIC_FONT = "Times-Italic"

    # Page settings
    PAGE_SIZE = A4
    PAGE_WIDTH, PAGE_HEIGHT = A4

    @classmethod
    def get_table_layout(cls):
        table_width = sum(cls.TABLE_COL_WIDTHS)
        page_center = cls.PAGE_WIDTH / 2
        table_center_x = page_center - table_width / 2
        return table_width, table_center_x 