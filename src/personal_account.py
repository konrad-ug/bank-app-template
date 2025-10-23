from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50 if self.is_promo_code_valid(promo_code) else 0.0
        
    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        return False
    
    def is_owner_born_after_1960(self):
        if self.pesel == "Invalid":
            return False
        year_prefix = '19' if int(self.pesel[2:4]) < 60 else '20'
        birth_year = int(year_prefix + self.pesel[0:2])
        return birth_year > 1960