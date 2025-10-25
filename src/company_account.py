from src.account import Account

class CompanyAccount(Account):
    express_outgoing_transfer_fee = 5.0
    
    def __init__(self, company_name: str, nip: str):
        self.name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0.0
        
    def is_nip_valid(self, nip) -> bool:
        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            return True
        return False