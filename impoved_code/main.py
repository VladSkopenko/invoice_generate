from typing import List, Dict, Any
from .models.invoice_data import InvoiceData, CompanyInfo, BankDetails, LineItem
from .renderers.invoice_renderer import InvoiceRenderer


class InvoiceGenerator:
    """Генератор счетов-фактур с улучшенной архитектурой"""
    
    def __init__(self):
        self.renderer = InvoiceRenderer()

    def generate_invoice(self, **kwargs) -> None:
        """
        Генерация счета-фактуры (совместимость со старым API)
        
        Args:
            **kwargs: Параметры счета в старом формате
        """
        # Валидация входных данных
        errors = self.validation_service.validate_legacy_data(kwargs)
        if errors:
            raise ValueError(f"Ошибки валидации: {', '.join(errors)}")

        # Преобразование в новую структуру данных
        invoice_data = self._convert_legacy_data(kwargs)
        
        # Отрисовка счета
        self.renderer.render(invoice_data, kwargs['filename'])

    def generate_invoice_from_data(self, invoice_data: InvoiceData, filename: str) -> None:
        """
        Генерация счета-фактуры из структурированных данных
        
        Args:
            invoice_data: Данные счета
            filename: Имя файла для сохранения
        """
        self.renderer.render(invoice_data, filename)

    def _convert_legacy_data(self, data: Dict[str, Any]) -> InvoiceData:
        """Преобразование старых данных в новую структуру"""
        
        # Создание объектов компаний
        seller = CompanyInfo(
            name=data['company_seller_name'],
            edprou=data['company_seller_edprou'],
            address=data['company_seller_address'],
            country=data['company_seller_country']
        )
        
        buyer = CompanyInfo(
            name=data['company_buyer_name'],
            edprou=data['client_buyer_edprou'],
            address=data['client_buyer_address'],
            country=data['client_buyer_country']
        )
        
        # Создание банковских реквизитов
        bank = BankDetails(
            name=data['bank_name_seller'],
            mfo=data['bank_mfo_seller'],
            address=data['bank_address_seller'],
            swift=data['bank_swift_seller'],
            iban=data['bank_iban_seller']
        )
        
        # Создание товарных позиций
        line_items = []
        for item_data in data['line_items']:
            line_item = LineItem(
                description=item_data['description'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
            line_items.append(line_item)
        
        # Создание объекта счета
        invoice_data = InvoiceData(
            seller=seller,
            buyer=buyer,
            bank=bank,
            invoice_number=data['invoice_number'],
            invoice_date=data['invoice_date'],
            due_date=data['due_date'],
            source=data['source'],
            line_items=line_items,
            vat_rate=data.get('vat_rate', 20),
            currency=data.get('currency', 'USD')
        )
        
        return invoice_data

    def create_invoice_data(
        self,
        seller: CompanyInfo,
        buyer: CompanyInfo,
        bank: BankDetails,
        invoice_number: str,
        invoice_date: str,
        due_date: str,
        source: str,
        line_items: List[LineItem],
        vat_rate: float = 20.0,
        currency: str = "USD"
    ) -> InvoiceData:
        """
        Создание объекта данных счета
        
        Args:
            seller: Информация о продавце
            buyer: Информация о покупателе
            bank: Банковские реквизиты
            invoice_number: Номер счета
            invoice_date: Дата счета
            due_date: Срок оплаты
            source: Источник
            line_items: Товарные позиции
            vat_rate: Ставка НДС
            currency: Код валюты
            
        Returns:
            InvoiceData: Объект данных счета
        """
        return InvoiceData(
            seller=seller,
            buyer=buyer,
            bank=bank,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            due_date=due_date,
            source=source,
            line_items=line_items,
            vat_rate=vat_rate,
            currency=currency
        ) 