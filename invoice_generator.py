from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

class InvoiceGenerator:
    """Класс для генерации PDF рахунків-фактур на українській мові"""
    
    def __init__(self):
        """Ініціалізація генератора рахунків"""
        self.fonts_registered = False
        self.register_times_fonts()
        
        # Налаштування шрифтів
        self.title_font = "Times-Bold"
        self.normal_font = "Times"
        self.bold_font = "Times-Bold"
        self.italic_font = "Times-Italic"
        
        # Кольори
        self.primary_color = colors.HexColor("#800080")  # Purple
        self.text_color = colors.black
        self.white_color = colors.white
    
    def register_times_fonts(self):
        """Реєстрація шрифтів Times з папки fonts"""
        if self.fonts_registered:
            return
            
        fonts_dir = "fonts"
        
        # Визначення шрифтів
        font_files = {
            "Times": "TIMES.TTF",
            "Times-Bold": "TIMESBD.TTF", 
            "Times-Italic": "TIMESI.TTF",
            "Times-BoldItalic": "TIMESBI.TTF"
        }
        
        # Реєстрація кожного шрифту
        for font_name, font_file in font_files.items():
            font_path = os.path.join(fonts_dir, font_file)
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    print(f"Зареєстровано шрифт: {font_name}")
                except Exception as e:
                    print(f"Помилка реєстрації {font_name}: {e}")
            else:
                print(f"Файл шрифту не знайдено: {font_path}")
        
        self.fonts_registered = True
    
    def generate_invoice(self, filename, 
                        # Дані компанії (хто виставляє рахунок)
                        company_name="ТОВ 'Моя Компанія'",
                        company_edprou="12345678",
                        company_address="м. Київ, вул. Хрещатик, 1",
                        
                        # Банківські реквізити
                        bank_name="ПриватБанк",
                        bank_mfo="305299",
                        bank_address="м. Дніпро, вул. Набережна Перемоги, 50",
                        bank_swift="PBANUA2X",
                        bank_iban="UA123456789012345678901234567",
                        
                        # Дані клієнта (кому виставляють рахунок)
                        client_name="ТОВ 'Клієнт Компанія'",
                        client_edprou="87654321",
                        client_address="м. Львів, вул. Свободи, 15",
                        
                        # Деталі рахунку
                        invoice_number="РФ/2024/00001",
                        invoice_date="15.01.2024",
                        
                        # Товари/послуги
                        line_items=None,
                        
                        # ПДВ
                        vat_rate=20,
                        
                        # Логотип
                        logo_path=None):
        
        """Генерація PDF рахунку-фактури"""
        
        # Товари за замовчуванням
        if line_items is None:
            line_items = [
                {
                    "description": "Послуги з розробки програмного забезпечення",
                    "quantity": 1.00,
                    "unit_price": 10000.00
                }
            ]
        
        # Створення PDF
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # Розміщення логотипу
        company_start_y = self._draw_logo(c, logo_path, height)
        
        # Дані компанії (ліворуч)
        self._draw_company_info(c, company_name, company_edprou, company_address, company_start_y)
        
        # Дані клієнта (праворуч)
        self._draw_client_info(c, client_name, client_edprou, client_address, height)
        
        # Заголовок рахунку
        self._draw_invoice_header(c, invoice_number, height)
        
        # Дата
        self._draw_invoice_date(c, invoice_date, height)
        
        # Таблиця товарів
        subtotal, total_vat = self._draw_items_table(c, line_items, vat_rate, height)
        
        # Підсумки
        self._draw_totals(c, subtotal, total_vat, vat_rate, height)
        
        # Банківські реквізити
        self._draw_bank_details(c, bank_name, bank_mfo, bank_address, bank_swift, bank_iban, height)
        
        # Футер з платформою
        self._draw_footer(c, width, height)
        
        # Збереження
        c.save()
    
    def _draw_logo(self, canvas, logo_path, height):
        """Отрисовка логотипу"""
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=1.5*inch, height=0.5*inch)
                logo.drawOn(canvas, 50, height - 80)
                return height - 120
            except:
                pass
        
        # Текстовий логотип як запасний варіант
        canvas.setFont(self.title_font, 20)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(50, height - 50, "КОМПАНІЯ")
        return height - 70
    
    def _draw_company_info(self, canvas, name, edprou, address, start_y):
        """Отрисовка інформації про компанію"""
        canvas.setFont(self.normal_font, 10)
        canvas.setFillColor(self.text_color)
        
        canvas.drawString(50, start_y, name)
        canvas.drawString(50, start_y - 15, f"ЄДРПОУ: {edprou}")
        canvas.drawString(50, start_y - 30, address)
    
    def _draw_client_info(self, canvas, name, edprou, address, height):
        """Отрисовка інформації про клієнта"""
        canvas.setFont(self.normal_font, 10)
        canvas.setFillColor(self.text_color)
        
        canvas.drawString(350, height - 70, name)
        canvas.drawString(350, height - 85, f"ЄДРПОУ: {edprou}")
        canvas.drawString(350, height - 100, address)
    
    def _draw_invoice_header(self, canvas, invoice_number, height):
        """Отрисовка заголовку рахунку"""
        canvas.setFont(self.title_font, 14)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(50, height - 160, f"Рахунок-фактура {invoice_number}")
    
    def _draw_invoice_date(self, canvas, invoice_date, height):
        """Отрисовка дати рахунку"""
        canvas.setFont(self.normal_font, 10)
        canvas.setFillColor(self.text_color)
        canvas.drawString(50, height - 180, f"Дата: {invoice_date}")
    
    def _draw_items_table(self, canvas, line_items, vat_rate, height):
        """Отрисовка таблиці товарів"""
        subtotal = 0
        
        # Підготовка даних таблиці
        table_data = [["Опис", "Кількість", "Ціна", "Сума"]]
        
        for item in line_items:
            quantity = item["quantity"]
            unit_price = item["unit_price"]
            amount = quantity * unit_price
            
            subtotal += amount
            
            table_data.append([
                item["description"],
                f"{quantity:.2f}",
                f"{unit_price:.2f} грн",
                f"{amount:.2f} грн"
            ])
        
        # Створення таблиці
        table = Table(table_data, colWidths=[250, 60, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.white_color),
            ('GRID', (0,0), (-1,-1), 0.25, self.text_color),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTNAME', (0,0), (-1,0), self.bold_font),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('FONTNAME', (0,1), (-1,-1), self.normal_font),
            ('FONTSIZE', (0,1), (-1,-1), 9),
        ]))
        
        table.wrapOn(canvas, A4[0], A4[1])
        table.drawOn(canvas, 50, height - 250)
        
        total_vat = subtotal * (vat_rate / 100)
        return subtotal, total_vat
    
    def _draw_totals(self, canvas, subtotal, total_vat, vat_rate, height):
        """Отрисовка підсумків"""
        total = subtotal + total_vat
        
        canvas.setFont(self.normal_font, 10)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(350, height - 270, f"Сума без ПДВ:")
        canvas.drawString(350, height - 285, f"ПДВ {vat_rate}%:")
        canvas.setFont(self.bold_font, 12)
        canvas.drawString(350, height - 300, "Всього:")
        
        canvas.setFont(self.normal_font, 10)
        canvas.setFillColor(self.text_color)
        canvas.drawString(450, height - 270, f"{subtotal:.2f} грн")
        canvas.drawString(450, height - 285, f"{total_vat:.2f} грн")
        canvas.setFont(self.bold_font, 12)
        canvas.drawString(450, height - 300, f"{total:.2f} грн")
    
    def _draw_bank_details(self, canvas, bank_name, bank_mfo, bank_address, bank_swift, bank_iban, height):
        """Отрисовка банківських реквізитів"""
        canvas.setFont(self.bold_font, 11)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(50, height - 320, "Банківські реквізити:")
        
        canvas.setFont(self.normal_font, 9)
        canvas.setFillColor(self.text_color)
        canvas.drawString(50, height - 335, f"Банк: {bank_name}")
        canvas.drawString(50, height - 350, f"МФО: {bank_mfo}")
        canvas.drawString(50, height - 365, f"Адреса: {bank_address}")
        canvas.drawString(50, height - 380, f"SWIFT: {bank_swift}")
        canvas.drawString(50, height - 395, f"IBAN: {bank_iban}")
    
    def _draw_footer(self, canvas, width, height):
        """Отрисовка футера"""
        canvas.line(50, 80, width - 50, 80)
        
        # Інформація про платформу
        canvas.setFont(self.normal_font, 9)
        canvas.setFillColor(self.text_color)
        canvas.drawCentredString(width / 2, 60, "Рахунок створений платформою https://inbulk.com")

# Приклад використання
if __name__ == "__main__":
    # Створення екземпляру генератора
    generator = InvoiceGenerator()
    
    # Генерація рахунку
    generator.generate_invoice(
        filename="invoice.pdf",
        company_name="ТОВ 'Технології Майбутнього'",
        company_edprou="12345678",
        company_address="м. Київ, вул. Велика Васильківська, 100",
        bank_name="ПриватБанк",
        bank_mfo="305299",
        bank_address="м. Дніпро, вул. Набережна Перемоги, 50",
        bank_swift="PBANUA2X",
        bank_iban="UA123456789012345678901234567",
        client_name="ТОВ 'Інноваційні Рішення'",
        client_edprou="87654321",
        client_address="м. Львів, вул. Свободи, 15",
        invoice_number="РФ/2024/00001",
        invoice_date="15.01.2024",
        line_items=[
            {
                "description": "Розробка веб-сайту",
                "quantity": 1.00,
                "unit_price": 15000.00
            },
            {
                "description": "Технічна підтримка (30 днів)",
                "quantity": 1.00,
                "unit_price": 5000.00
            }
        ],
        vat_rate=20
    )
