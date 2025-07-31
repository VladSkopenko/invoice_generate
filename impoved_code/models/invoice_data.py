from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class CompanyInfo:
    name: str
    edprou: str
    address: str
    country: str


@dataclass
class BankDetails:
    name: str
    mfo: str
    address: str
    swift: str
    iban: str


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float

    def get_amount(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class InvoiceData:
    seller: CompanyInfo
    buyer: CompanyInfo
    bank: BankDetails
    
  
    invoice_number: str
    invoice_date: str
    due_date: str
    source: str
    
    line_items: List[LineItem]
    vat_rate: float = 20.0
    currency: str = "USD"
    
    def get_subtotal(self) -> float:
        """Получить сумму без НДС"""
        return sum(item.get_amount() for item in self.line_items)
    
    def get_vat_amount(self) -> float:
        """Получить сумму НДС"""
        return self.get_subtotal() * (self.vat_rate / 100)
    
    def get_total(self) -> float:
        """Получить общую сумму"""
        return self.get_subtotal() + self.get_vat_amount()
    
    def get_line_items_dict(self) -> List[Dict]:
        """Получить товарные позиции в виде словарей для совместимости"""
        return [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price
            }
            for item in self.line_items
        ] 