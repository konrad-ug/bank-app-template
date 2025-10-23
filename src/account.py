class Account:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount
            
    def outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount