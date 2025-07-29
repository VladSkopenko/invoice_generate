from invoice_generator import InvoiceGenerator

# Простий приклад використання
def create_my_invoice():
    # Створення екземпляру генератора
    generator = InvoiceGenerator()
    
    # Генерація рахунку
    generator.generate_invoice(
        filename="my_invoice.pdf",
        
        # Дані компанії (продавець)
        company_name="ТОВ 'Моя Компанія'",
        company_edprou="12345678",
        company_address="м. Київ, вул. Хрещатик, 1",
        
        # Банківські реквізити
        bank_name="ПриватБанк",
        bank_mfo="305299",
        bank_address="м. Дніпро, вул. Набережна Перемоги, 50",
        bank_swift="PBANUA2X",
        bank_iban="UA123456789012345678901234567",
        
        # Дані клієнта (покупець)
        client_name="ТОВ 'Клієнт Компанія'",
        client_edprou="87654321",
        client_address="м. Львів, вул. Свободи, 15",
        
        # Деталі рахунку
        invoice_number="РФ/2024/00001",
        invoice_date="15.01.2024",
        
        # Товари/послуги
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
        
        # ПДВ
        vat_rate=20
    )

def create_simple_invoice():
    """Приклад створення простого рахунку з мінімальними даними"""
    generator = InvoiceGenerator()
    
    generator.generate_invoice(
        filename="simple_invoice.pdf",
        company_name="ТОВ 'Проста Компанія'",
        company_edprou="11111111",
        company_address="м. Харків, вул. Сумська, 1",
        bank_name="Ощадбанк",
        bank_mfo="300465",
        bank_address="м. Київ, вул. Госпітальна, 12г",
        bank_swift="COSCUAUK",
        bank_iban="UA123456789012345678901234567",
        client_name="ТОВ 'Простий Клієнт'",
        client_edprou="22222222",
        client_address="м. Одеса, вул. Дерибасівська, 1",
        invoice_number="РФ/2024/00002",
        invoice_date="16.01.2024",
        line_items=[
            {
                "description": "Простий товар",
                "quantity": 1.00,
                "unit_price": 1000.00
            }
        ],
        vat_rate=20
    )

def create_multiple_invoices():
    """Приклад створення кількох рахунків з одним екземпляром генератора"""
    generator = InvoiceGenerator()
    
    # Перший рахунок
    generator.generate_invoice(
        filename="invoice_1.pdf",
        company_name="ТОВ 'Компанія А'",
        company_edprou="33333333",
        company_address="м. Дніпро, вул. Набережна, 1",
        bank_name="Укргазбанк",
        bank_mfo="300023",
        bank_address="м. Київ, вул. Хрещатик, 8",
        bank_swift="UGASUAUK",
        bank_iban="UA123456789012345678901234567",
        client_name="ТОВ 'Клієнт А'",
        client_edprou="44444444",
        client_address="м. Запоріжжя, вул. Соборна, 1",
        invoice_number="РФ/2024/00003",
        invoice_date="17.01.2024",
        line_items=[
            {
                "description": "Товар А",
                "quantity": 2.00,
                "unit_price": 500.00
            }
        ],
        vat_rate=20
    )
    
    # Другий рахунок
    generator.generate_invoice(
        filename="invoice_2.pdf",
        company_name="ТОВ 'Компанія Б'",
        company_edprou="55555555",
        company_address="м. Полтава, вул. Соборності, 1",
        bank_name="Райффайзен Банк",
        bank_mfo="380805",
        bank_address="м. Київ, вул. Подільська, 13",
        bank_swift="AVALUAUK",
        bank_iban="UA123456789012345678901234567",
        client_name="ТОВ 'Клієнт Б'",
        client_edprou="66666666",
        client_address="м. Суми, вул. Петропавлівська, 1",
        invoice_number="РФ/2024/00004",
        invoice_date="18.01.2024",
        line_items=[
            {
                "description": "Товар Б",
                "quantity": 3.00,
                "unit_price": 750.00
            }
        ],
        vat_rate=20
    )

if __name__ == "__main__":
    create_my_invoice()

