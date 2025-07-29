# Invoice Generator

Генератор рахунків-фактур на Python з використанням ReportLab для створення професійних PDF документів.

## Опис

Цей проект дозволяє створювати рахунки-фактури з автоматичним розрахунком ПДВ, підтримкою довгих описів товарів з автоматичним переносом тексту та гнучкою конфігурацією макету.

## Особливості

- ✅ **Професійний дизайн** - чистий макет без зайвих рамок
- ✅ **Автоматичний перенос тексту** - довгі описи товарів переносяться автоматично
- ✅ **Динамічне позиціонування** - таблиця правильно розширюється при додаванні товарів
- ✅ **Гнучка конфігурація** - всі параметри винесені в класові змінні
- ✅ **Підтримка української мови** - вбудовані шрифти Times New Roman
- ✅ **Автоматичний розрахунок** - ПДВ та загальна сума розраховуються автоматично

## Встановлення

1. Клонуйте репозиторій:
```bash
git clone <repository-url>
cd generation_invoice
```

2. Встановіть залежності:
```bash
pip install -r requirements.txt
```

## Використання

### Базовий приклад

```python
from invoice_generator import InvoiceGenerator

# Створюємо екземпляр генератора
generator = InvoiceGenerator()

# Генеруємо рахунок
generator.generate_invoice(
    filename="invoice.pdf",
    company_name="ТОВ 'Моя Компанія'",
    company_edprou="12345678",
    company_address="м. Київ, вул. Хрещатик, 1",
    company_country="Україна",
    client_name="ТОВ 'Клієнт Компанія'",
    client_edprou="87654321",
    client_address="м. Львів, вул. Свободи, 15",
    client_country="Україна",
    invoice_number="INV/2024/00007",
    invoice_date="22/02/2024",
    due_date="22/02/2024",
    source="S00007",
    vat_rate=20
)
```

### Приклад з власними товарами

```python
line_items = [
    {
        "description": "Послуги з розробки програмного забезпечення",
        "quantity": 1,
        "unit_price": 10000
    },
    {
        "description": "Технічна підтримка протягом місяця",
        "quantity": 1,
        "unit_price": 5000
    },
    {
        "description": "Дуже довгий опис товару з багатьма словами для тестування автоматичного переносу тексту",
        "quantity": 2,
        "unit_price": 1500
    }
]

generator.generate_invoice(
    filename="custom_invoice.pdf",
    line_items=line_items,
    vat_rate=20,
    # ... інші параметри
)
```

## Параметри методу generate_invoice

| Параметр | Тип | Опис | За замовчуванням |
|----------|-----|------|------------------|
| `filename` | str | Назва файлу PDF | - |
| `company_name` | str | Назва компанії-продавця | "ТОВ 'Моя Компанія'" |
| `company_edprou` | str | ЄДРПОУ продавця | "12345678" |
| `company_address` | str | Адреса продавця | "м. Київ, вул. Хрещатик, 1" |
| `company_country` | str | Країна продавця | "Україна" |
| `bank_name` | str | Назва банку | "ПриватБанк" |
| `bank_mfo` | str | МФО банку | "305299" |
| `bank_address` | str | Адреса банку | "м. Дніпро, вул. Набережна Перемоги, 50" |
| `bank_swift` | str | SWIFT код банку | "PBANUA2X" |
| `bank_iban` | str | IBAN рахунку | "UA123456789012345678901234567" |
| `client_name` | str | Назва клієнта-покупця | "ТОВ 'Клієнт Компанія'" |
| `client_edprou` | str | ЄДРПОУ покупця | "87654321" |
| `client_address` | str | Адреса покупця | "м. Львів, вул. Свободи, 15" |
| `client_country` | str | Країна покупця | "Україна" |
| `invoice_number` | str | Номер рахунку | "INV/2024/00007" |
| `invoice_date` | str | Дата рахунку | "22/02/2024" |
| `due_date` | str | Термін оплати | "22/02/2024" |
| `source` | str | Джерело | "S00007" |
| `line_items` | list | Список товарів/послуг | None (використовуються тестові дані) |
| `vat_rate` | int | Ставка ПДВ (%) | 15 |

## Структура line_items

Кожен елемент у списку `line_items` повинен містити:

```python
{
    "description": "Опис товару або послуги",
    "quantity": 1.0,  # Кількість
    "unit_price": 100.0  # Ціна за одиницю
}
```

## Налаштування макету

Всі параметри макету можна налаштувати через класові змінні:

```python
# Відступи від країв сторінки
MARGIN_LEFT = 50
MARGIN_RIGHT = 50
MARGIN_TOP = 30
MARGIN_BOTTOM = 80

# Розміри шрифтів
FONT_SIZE_TITLE = 24
FONT_SIZE_HEADER = 20
FONT_SIZE_SUBHEADER = 14
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 11
FONT_SIZE_FOOTER = 9

# Ширина колонок таблиці
TABLE_COL_WIDTHS = [250, 80, 100, 35, 115]

# Координати для секції підсумків
TOTALS_START_X = 300
TOTALS_END_X = 580
```

## Структура проекту

```
generation_invoice/
├── invoice_generator.py    # Основний клас генератора
├── example_usage.py        # Приклад використання
├── requirements.txt        # Залежності проекту
├── fonts/                  # Шрифти Times New Roman
│   ├── TIMES.TTF
│   ├── TIMESBD.TTF
│   ├── TIMESBI.TTF
│   └── TIMESI.TTF
└── README.md              # Цей файл
```

## Залежності

- `reportlab==4.0.7` - бібліотека для створення PDF документів

