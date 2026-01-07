from datetime import datetime
from lib.smtp import SMTPClient


class Account:
    express_outgoing_transfer_fee = 0.0
    history_email_text_template = "Account history:"
    def __init__(self):
        self.history = []

    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)
            return True
            
    def outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)
            return True
        return False
    
    def express_outgoing_transfer(self, amount):
        if amount <= 0:
            return False
        if amount <= self.balance:
            self.balance -= amount + self.express_outgoing_transfer_fee
            self.history.append(-amount)
            self.history.append(-self.express_outgoing_transfer_fee)
            return True
        return False
            
    def send_history_via_email(self, email_address: str) -> bool:
        today_date = datetime.today().strftime('%Y-%m-%d')
        subject = "Account Transfer History " + today_date
        text = self.history_email_text_template + self.history.__str__()
        return SMTPClient.send(subject, text, email_address)