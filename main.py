from impoved_code.renderers.invoice_renderer import InvoiceRenderer
from impoved_code.models.invoice_data import InvoiceData, CompanyInfo, BankDetails, LineItem
from decimal import Decimal


if __name__ == "__main__":
    renderer = InvoiceRenderer()
    
    # Create sample invoice data
    seller = CompanyInfo(
        name="ТОВ 'Технологічні Рішення'",
        edprou="12345678",
        address="вул. Інноваційна, 123, м. Київ, 01001",
        country="Україна"
    )
    
    buyer = CompanyInfo(
        name="ТОВ 'Цифрові Інновації'",
        edprou="87654321",
        address="просп. Бізнес, 456, м. Львів, 79000",
        country="Україна"
    )
    
    bank = BankDetails(
        name="ПриватБанк",
        mfo="305299",
        address="просп. Дмитра Яворницького, 1, м. Дніпро, 49000",
        swift="PBANUA2X",
        iban="UA123456789012345678901234567"
    )
    
    line_items = [
        LineItem(
            description="10% передоплата",
            quantity=Decimal("1.0"),
            unit_price=Decimal("1000.00")
        ),
        LineItem(
            description="25% після завантаження авто",
            quantity=Decimal("1.0"),
            unit_price=Decimal("2500.00")
        ),
        LineItem(
            description="65% післяплата",
            quantity=Decimal("1.0"),
            unit_price=Decimal("6500.00")
        )
    ]
    
    invoice_data = InvoiceData(
        seller=seller,
        buyer=buyer,
        bank=bank,
        invoice_number="РФ-2024-001",
        invoice_date="2024-01-15",
        due_date="2024-02-15",
        source="Договір №2024-001",
        line_items=line_items,
        vat_rate=Decimal("20.0"),
        currency="UAH"
    )
    
    renderer.render(invoice_data, "invoice.pdf")