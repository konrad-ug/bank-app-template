from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestTransfers:
    
    def test_incoming_transfer(self):
        account = PersonalAccount("John", "Doe", "12345678901") #1. set up
        account.incoming_transfer(100.0) # 2. action
        assert account.balance == 100.0 # 3. assertion
        
    def test_outgoing_transfer(self):
        account = PersonalAccount("John", "Doe", "12345678901") #1. set up
        account.balance = 70.0 #1. set up
        account.outgoing_transfer(50.0) # 2. action
        assert account.balance == 20.0 # 3. assertion
    
    def test_incoming_transfer_negative_amount(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming_transfer(-50.0)
        assert account.balance == 0.0
        
    def test_outgoing_transfer_zero_balance(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.outgoing_transfer(50.0)
        assert account.balance == 0.0
    
    def test_outgoing_transfer_negativ_amount(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming_transfer(100.0)
        account.outgoing_transfer(-30.0)
        assert account.balance == 100.0
        
    def test_outgoing_transfer_sufficient_balance(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 100.0
        account.outgoing_transfer(40.0)
        assert account.balance == 60.0

    def test_outgoing_transfer_insufficient_balance(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming_transfer(100.0)
        account.outgoing_transfer(150.0)
        assert account.balance == 100.0
        
    def test_company_account_incoming_transfer(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        company_account.incoming_transfer(200.0)
        assert company_account.balance == 200.0
        
    def test_company_account_outgoing_transfer(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        company_account.balance = 300.0
        company_account.outgoing_transfer(100.0)
        assert company_account.balance == 200.0
        
    def test_company_account_outgoing_transfer_insufficient_balance(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        company_account.incoming_transfer(150.0)
        company_account.outgoing_transfer(200.0)
        assert company_account.balance == 150.0
        
    def test_personal_account_express_transfer(self):
        personal_account = PersonalAccount("Emily", "Clark", "09876543210")
        personal_account.balance = 120.0
        personal_account.express_outgoing_transfer(70.0)
        assert personal_account.balance == 49.0
        
    def test_personal_account_express_transfer_insufficient_balance(self):
        personal_account = PersonalAccount("Emily", "Clark", "09876543210")
        personal_account.balance = 50.0
        personal_account.express_outgoing_transfer(60.0)
        assert personal_account.balance == 50.0

    def test_company_account_outgoing_express_transfer(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        company_account.balance = 300.0
        company_account.express_outgoing_transfer(100.0)
        assert company_account.balance == 195.0
        
    def test_company_account_express_transfer_insufficient_balance(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        company_account.balance = 80.0
        company_account.express_outgoing_transfer(90.0)
        assert company_account.balance == 80.0
