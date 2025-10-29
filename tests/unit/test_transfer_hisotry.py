from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfersHistory:
    
    def test_incoming_transfer_history(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming_transfer(100.0)
        assert account.history == [100.0]
        
    def test_outgoing_transfer_history(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 150.0
        account.outgoing_transfer(50.0)
        assert account.history == [-50.0]
        
    def test_express_outgoing_transfer_history(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 200.0
        account.express_outgoing_transfer(70.0)
        assert account.history == [-70.0, - account.express_outgoing_transfer_fee]
        
    def test_series_of_transfers_history(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming_transfer(200.0)
        account.outgoing_transfer(50.0)
        account.express_outgoing_transfer(80.0)
        assert account.history == [200.0, -50.0, -80.0, - account.express_outgoing_transfer_fee]