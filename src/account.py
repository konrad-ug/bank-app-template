class Account:
    express_outgoing_transfer_fee = 0.0
        
    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount
            
    def outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            
    def express_outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount + self.express_outgoing_transfer_fee