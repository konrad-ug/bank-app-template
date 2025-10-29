
class Account:
    express_outgoing_transfer_fee = 0.0
    def __init__(self):
        self.history = []

    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)
            
    def outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)
               
    def express_outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount + self.express_outgoing_transfer_fee
            self.history.append(-amount)
            self.history.append(-self.express_outgoing_transfer_fee)
            
    def print_coverage(self):
        for transaction in self.history:
            print(transaction)