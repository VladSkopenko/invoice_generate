# Перенесено
class CurrencyMapping:
    CURRENCY_MAPPING = {
        "USD": "$",     
        "UAH": "₴",     
        "EUR": "€", 
        "GBP": "£", 
        "JPY": "¥",      
        "PLN": "zł",     
        "CZK": "Kč",
        "HUF": "Ft",
        "RON": "lei",  
        "BGN": "лв",    
        "HRK": "kn",     
        "DKK": "kr",   
        "SEK": "kr",  
        "NOK": "kr",    
        "CHF": "CHF",    
        "CNY": "¥",   
        "INR": "₹",    
        "BRL": "R$",    
        "CAD": "C$",    
        "AUD": "A$",    
        "NZD": "NZ$",    
        "KRW": "₩",   
        "SGD": "S$",   
        "HKD": "HK$", 
        "BTC": "₿",
        "ETH": "Ξ",
    }

    @classmethod
    def get_symbol(cls, currency_code: str) -> str:
        return cls.CURRENCY_MAPPING.get(currency_code.upper(), currency_code) 