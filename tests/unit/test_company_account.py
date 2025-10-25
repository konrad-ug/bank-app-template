from src.company_account import CompanyAccount

class TestCompanyAccount:
    
    def test_company_account_creation(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        assert company_account.name == "Tech Solutions"
        assert company_account.balance == 0.0
        assert company_account.nip == "1234567890"
        
    def test_nip_too_long(self):
        company_account = CompanyAccount("Business Corp", "1234567890123")
        assert company_account.nip == "Invalid"
        
    def test_nip_too_short(self):
        company_account = CompanyAccount("Business Corp", "12345")
        assert company_account.nip == "Invalid"
        
    def test_nip_none(self):
        company_account = CompanyAccount("Business Corp", None)
        assert company_account.nip == "Invalid"
        
    def test_nip_with_non_digit_characters(self):
        company_account = CompanyAccount("Business Corp", "12345A7890")
        assert company_account.nip == "Invalid"