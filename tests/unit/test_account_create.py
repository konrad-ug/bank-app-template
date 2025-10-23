from src.personal_account import PersonalAccount


class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"
        
    def test_pesel_too_long(self):
        account = PersonalAccount("Jane", "Doe", "123456789013e23")
        assert account.pesel == "Invalid"
        
    def test_pesel_too_short(self):
        account = PersonalAccount("Jane", "Doe", "123")
        assert account.pesel == "Invalid"
        
    def test_pesel_none(self):
        account = PersonalAccount("Jane", "Doe", None)
        assert account.pesel == "Invalid"
        
    def test_correct_promo_code(self):
        account = PersonalAccount("Alice", "Smith", "12345678901", "PROM_123")
        assert account.balance == 50.0
        
    def test_promo_code_suffix_too_long(self):
        account = PersonalAccount("Alice", "Smith", "12345678901", "PROM_XYZZ")
        assert account.balance == 0.0
        
    def test_promo_code_suffix_too_short(self):
        account = PersonalAccount("Alice", "Smith", "12345678901", "PROM_XY")
        assert account.balance == 0.0
        
    def test_wrong_prefix_minus(self):
        account = PersonalAccount("Alice", "Smith", "12345678901", "PROM-XYZ")
        assert account.balance == 0.0

    def test_wrong_prefix(self):
        account = PersonalAccount("Alice", "Smith", "12345678901", "PPOM-XYZ")
        assert account.balance == 0.0