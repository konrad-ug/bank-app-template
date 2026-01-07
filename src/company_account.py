from datetime import datetime
from src.account import Account
import requests
import os

class CompanyAccount(Account):
    express_outgoing_transfer_fee = 5.0
    history_email_text_template = "Company account history:"
    BANK_APP_MF_URL = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
    
    def __init__(self, company_name: str, nip: str):
        super().__init__()
        self.name = company_name
        if not self.is_nip_valid(nip):
            self.nip = "Invalid"
        elif self.is_nip_active_in_MF_registry(nip):
            self.nip = nip
        else:
            raise ValueError("NIP is not active in MF registry")
        self.balance = 0.0
        self.history = []
        
    def is_nip_valid(self, nip) -> bool:
        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            return True
        return False
    
    def submit_for_loan(self, amount: float) -> bool:
        if self.balance < 2 * amount:
            return False
        if -1775 in self.history:
            self.balance += amount
            return True
        return False
    
    def is_nip_active_in_MF_registry(self, nip) -> bool:
        today_date = datetime.today().strftime('%Y-%m-%d')
        url = f"{self.BANK_APP_MF_URL}api/search/nip/{nip}?date={today_date}"
        print(f"sending requests to {url}")
        response = requests.get(url)
        print(f"Response status code: {response.json()}")
        if response.status_code != 200:
            return False

        data = response.json() or {}
        result = data.get("result") or {}
        subject = result.get("subject") or {}
        status = subject.get("statusVat")

        return status == "Czynny"

