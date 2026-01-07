import pytest
import requests

class TestCrudApi:
    url = "http://127.0.0.1:5000"
    account_data = {
        "name": "james",
        "surname": "hetfield",
        "pesel": "89092909825"
    }
    
    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        response = requests.post(f"{self.url}/api/accounts", json=self.account_data)
        assert response.status_code == 201
        yield
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/api/accounts/{pesel}")
    
    def test_get_account_count(self):
        response = requests.get(f"{self.url}/api/accounts/count")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1

    def test_create_account(self):
        new_account = {
            "name": "John",
            "surname": "Doe",
            "pesel": "12345678901"
        }
        response = requests.post(f"{self.url}/api/accounts", json=new_account)
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Account created"

    def test_delete_account(self):
        pesel_to_delete = self.account_data['pesel']
        response = requests.delete(f"{self.url}/api/accounts/{pesel_to_delete}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Account deleted"
        
    def test_create_account_with_already_existng_pesel(self):
        response = requests.post(f"{self.url}/api/accounts", json=self.account_data)
        assert response.status_code == 409
        data = response.json()
        assert data["message"] == "Account with this PESEL already exists"