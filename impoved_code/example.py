#!/usr/bin/env python3
"""
Пример использования улучшенного генератора счетов
"""

from main import InvoiceGenerator
from models.invoice_data import CompanyInfo, BankDetails, LineItem


def example_legacy_api():
    """Пример использования старого API (совместимость)"""
    print("=== Пример использования старого API ===")
    
    generator = InvoiceGenerator()
    
    generator.generate_invoice(
        filename="improved_invoice_uah.pdf",
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
                "description": "Програмне забезпечення для управління проектами",
                "quantity": 5,
                "unit_price": 100,
            },
            {
                "description": "Технічна підтримка (місяць)",
                "quantity": 1,
                "unit_price": 500,
            },
        ],
        vat_rate=20,
        currency="UAH",
    )
    print("Счет создан: improved_invoice_uah.pdf")


def example_new_api():
    """Пример использования нового API с структурированными данными"""
    print("\n=== Пример использования нового API ===")
    
    generator = InvoiceGenerator()
    
    # Создание данных компаний
    seller = CompanyInfo(
        name="ТОВ 'Технології Майбутнього'",
        edprou="12345678",
        address="м. Київ, вул. Велика Васильківська, 100",
        country="Україна"
    )
    
    buyer = CompanyInfo(
        name="ТОВ 'Інноваційні Рішення'",
        edprou="87654321",
        address="м. Львів, вул. Свободи, 15",
        country="Україна"
    )
    
    # Создание банковских реквизитов
    bank = BankDetails(
        name="ПриватБанк",
        mfo="305299",
        address="м. Дніпро, вул. Набережна Перемоги, 50",
        swift="PBANUA2X",
        iban="UA123456789012345678901234567"
    )
    
    # Создание товарных позиций
    line_items = [
        LineItem(
            description="Консультаційні послуги",
            quantity=10,
            unit_price=50
        ),
        LineItem(
            description="Дизайн веб-сайту",
            quantity=1,
            unit_price=1500
        )
    ]
    
    # Создание данных счета
    invoice_data = generator.create_invoice_data(
        seller=seller,
        buyer=buyer,
        bank=bank,
        invoice_number="РФ/2024/00002",
        invoice_date="15.01.2024",
        due_date="20.01.2024",
        source="S00002",
        line_items=line_items,
        vat_rate=20,
        currency="EUR"
    )
    
    # Генерация счета
    generator.generate_invoice_from_data(invoice_data, "improved_invoice_eur.pdf")
    print("Счет создан: improved_invoice_eur.pdf")


def example_validation():
    """Пример валидации данных"""
    print("\n=== Пример валидации данных ===")
    
    from services.validation import ValidationService
    
    # Тест с некорректными данными
    invalid_data = {
        'company_seller_name': '',  # Пустое имя
        'company_seller_edprou': '12345678',
        'company_seller_address': 'м. Київ',
        'company_seller_country': 'Україна',
        'company_buyer_name': 'ТОВ Тест',
        'client_buyer_edprou': '87654321',
        'client_buyer_address': 'м. Львів',
        'client_buyer_country': 'Україна',
        'bank_name_seller': 'ПриватБанк',
        'bank_mfo_seller': '305299',
        'bank_address_seller': 'м. Дніпро',
        'bank_swift_seller': 'PBANUA2X',
        'bank_iban_seller': 'UA123456789012345678901234567',
        'invoice_number': 'РФ/2024/00003',
        'invoice_date': '15.01.2024',
        'due_date': '20.01.2024',
        'source': 'S00003',
        'line_items': [
            {
                'description': 'Тест',
                'quantity': -1,  # Отрицательное количество
                'unit_price': 100
            }
        ]
    }
    
    errors = ValidationService.validate_legacy_data(invalid_data)
    print("Ошибки валидации:")
    for error in errors:
        print(f"  - {error}")


def example_currency_mapping():
    """Пример работы с валютами"""
    print("\n=== Пример работы с валютами ===")
    
    from config.currencies import CurrencyMapping
    
    currencies = ["USD", "UAH", "EUR", "GBP", "PLN", "BTC", "UNKNOWN"]
    
    for currency in currencies:
        symbol = CurrencyMapping.get_symbol(currency)
        print(f"{currency} -> {symbol}")


if __name__ == "__main__":
    # Копируем шрифты из основной папки
    import shutil
    import os
    
    if not os.path.exists("impoved_code/fonts"):
        shutil.copytree("../fonts", "impoved_code/fonts")
    
    # Запускаем примеры
    example_currency_mapping()
    example_validation()
    example_legacy_api()
    example_new_api()
    
    print("\n=== Все примеры выполнены! ===") 