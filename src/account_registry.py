from src.personal_account import PersonalAccount
from typing import List

class AccountRegistry:
    def __init__(self):
        self.accounts: List[PersonalAccount] = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None
    
    def get_all_accounts(self):
        return self.accounts
    
    def get_account_count(self):
        return len(self.accounts)
    
    def delete_account(self, pesel):
        self.accounts = [acc for acc in self.accounts if acc.pesel != pesel]
    
    