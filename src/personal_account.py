from calendar import month
from src.account import Account

class PersonalAccount(Account):
    express_outgoing_transfer_fee = 1.0
    
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50 if self.check_promotion_eligibility(pesel, promo_code) else 0.0
        
    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        
    def check_promotion_eligibility(self, pesel, promo_code):
        return self.is_owner_born_after_1960(pesel) and self.is_promo_code_valid(promo_code)
        
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        return False
    
    def is_owner_born_after_1960(self, pesel):
        if pesel == "Invalid" or pesel is None:
            return False
        month = int(pesel[2:4])
        year = int(pesel[0:2])
        if 1 <= month <= 12:
            year += 1900
        elif 21 <= month <= 32:
            year += 2000
        return year > 1960