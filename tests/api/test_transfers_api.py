import pytest
import requests

class TestTransfers:
    url = "http://127.0.0.1:5000"
    account_data = {
        "name": "james",
        "surname": "hetfield",
        "pesel": "89092909825"
    }
    incoming_transfer_data = {
            "amount": 1000,
            "type": "incoming"
    }
    
    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        response = requests.post(f"{self.url}/api/accounts", json=self.account_data)
        assert response.status_code == 201
        pesel = self.account_data['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=self.incoming_transfer_data)
        assert response.status_code == 200
        yield
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/api/accounts/{pesel}")
    
    def test_incoming_transfer(self):
        transfer_data = {
            "amount": 500,
            "type": "incoming"
        }
        pesel = self.account_data['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Transfer successful"
        
        # Verify the balance update
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        account_data = response.json()
        assert account_data["balance"] == self.incoming_transfer_data["amount"] + transfer_data["amount"]
        
    def test_outgoing_transfer_insufficient_funds(self):
        transfer_data = {
            "amount": 1200,
            "type": "outgoing"
        }
        pesel = self.account_data['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 422
        data = response.json()
        assert data["message"] == "There was an issue with transfer"
        
    def test_express_transfer(self):
        personal_account_fee = 1
        express_transfer_data = {
            "amount": 400,
            "type": "express"
        }
        pesel = self.account_data['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=express_transfer_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Transfer successful"
        
        # Verify the balance update considering express fee
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        account_data = response.json()
        expected_balance = 1000 - 400 - personal_account_fee
        assert account_data["balance"] == expected_balance  