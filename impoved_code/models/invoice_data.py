# Перенесено
from typing import List, Dict
from decimal import Decimal
from pydantic import BaseModel, Field, computed_field, validator
from datetime import date, datetime


class CompanyInfo(BaseModel):
    name: str = Field(..., description="Company name")
    edprou: str = Field(..., description="EDRPOU code")
    address: str = Field(..., description="Company address")
    country: str = Field(..., description="Country")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Example Company Ltd",
                "edprou": "12345678",
                "address": "123 Main St, Kyiv",
                "country": "Ukraine"
            }
        }


class BankDetails(BaseModel):
    name: str = Field(..., description="Bank name")
    mfo: str = Field(..., description="MFO code")
    address: str = Field(..., description="Bank address")
    swift: str = Field(..., description="SWIFT code")
    iban: str = Field(..., description="IBAN code")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "PrivatBank",
                "mfo": "305299",
                "address": "1 Dmytra Yavornytskoho Ave, Dnipro",
                "swift": "PBANUA2X",
                "iban": "UA123456789012345678901234567"
            }
        }


class LineItem(BaseModel):
    description: str = Field(..., description="Item description")
    quantity: Decimal = Field(..., gt=0, description="Quantity")
    unit_price: Decimal = Field(..., ge=0, description="Unit price")

    @computed_field
    @property
    def amount(self) -> Decimal:
        """Calculate the total amount for this line item."""
        return self.quantity * self.unit_price

    def to_dict(self) -> Dict[str, str | Decimal]:
        """Convert line item to dictionary representation."""
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount
        }

    @validator('quantity', 'unit_price', pre=True)
    def parse_decimals(cls, v):
        """Parse strings to Decimal if needed."""
        if isinstance(v, str):
            return Decimal(v)
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Web Development Services",
                "quantity": "10.0",
                "unit_price": "100.00"
            }
        }


class InvoiceData(BaseModel):
    seller: CompanyInfo = Field(..., description="Seller company information")
    buyer: CompanyInfo = Field(..., description="Buyer company information")
    bank: BankDetails = Field(..., description="Bank details")
    invoice_number: str = Field(..., description="Invoice number")
    invoice_date: date = Field(..., description="Invoice date")
    due_date: date = Field(..., description="Due date")
    source: str = Field(..., description="Source document")
    line_items: List[LineItem] = Field(default_factory=list, description="Line items")
    vat_rate: Decimal = Field(default=Decimal('20.0'), ge=0, le=100, description="VAT rate percentage")
    currency: str = Field(default="USD", description="Currency code")

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        """Calculate the subtotal of all line items."""
        return sum(item.amount for item in self.line_items)

    @computed_field
    @property
    def vat_amount(self) -> Decimal:
        """Calculate the VAT amount based on subtotal and VAT rate."""
        return self.subtotal * (self.vat_rate / Decimal('100'))

    @computed_field
    @property
    def total(self) -> Decimal:
        """Calculate the total amount including VAT."""
        return self.subtotal + self.vat_amount

    @computed_field
    @property
    def line_items_dict(self) -> List[Dict[str, str | Decimal]]:
        """Get line items as a list of dictionaries."""
        return [item.to_dict() for item in self.line_items]

    @validator('invoice_date', 'due_date', pre=True)
    def parse_dates(cls, v):
        """Parse date strings to date objects if needed."""
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                try:
                    return datetime.strptime(v, '%d.%m.%Y').date()
                except ValueError:
                    raise ValueError('Date must be in YYYY-MM-DD or DD.MM.YYYY format')
        return v

    @validator('vat_rate', pre=True)
    def parse_vat_rate(cls, v):
        """Parse VAT rate string to Decimal if needed."""
        if isinstance(v, str):
            return Decimal(v)
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "seller": {
                    "name": "Seller Company Ltd",
                    "edprou": "12345678",
                    "address": "123 Seller St, Kyiv",
                    "country": "Ukraine"
                },
                "buyer": {
                    "name": "Buyer Company Ltd",
                    "edprou": "87654321",
                    "address": "456 Buyer Ave, Lviv",
                    "country": "Ukraine"
                },
                "bank": {
                    "name": "PrivatBank",
                    "mfo": "305299",
                    "address": "1 Dmytra Yavornytskoho Ave, Dnipro",
                    "swift": "PBANUA2X",
                    "iban": "UA123456789012345678901234567"
                },
                "invoice_number": "INV-2024-001",
                "invoice_date": "2024-01-15",
                "due_date": "2024-02-15",
                "source": "Contract #123",
                "line_items": [
                    {
                        "description": "Web Development Services",
                        "quantity": "10.0",
                        "unit_price": "100.00"
                    }
                ],
                "vat_rate": "20.0",
                "currency": "USD"
            }
        } 