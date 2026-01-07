from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import pytest

class TestAccount:
    
    @pytest.fixture
    def mock_requests_get(self, mocker):
        mock = mocker.patch("src.company_account.requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        return mock

    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "89092909876")
        return account
    
    @pytest.mark.parametrize("history, amount, expected_result, expected_balance", [
        ([100, 100, 100], 500, True, 500),
        ([-100, 100, -100, 100, 1000], 700, True, 700),
        ([-100, 20000, -100, 100, -1000], 1000, True, 1000),
        ([100], 666, False, 0),
        ([-100, 100, 100, 100, -6000, 200], 500, False , 0),
    ])
    def test_loan(self, account: PersonalAccount, history, amount, expected_result, expected_balance):
        account.history = history
        result = account.submit_for_loan(amount)
        assert result == expected_result
        assert account.balance == expected_balance
        
    company_loan_tests = [
        ([4000, -1775, 2000], 4000, 2000, True, 6000),
        ([5000, -1775, -1000, 3000], 6000, 2500, True, 8500),
        ([3000, 1000, -1775], 3000, 5000, False, 3000),
        ([6000, -1000, 4000], 6000, 4000, False, 6000),
    ]
    ids = [
        "sufficient balance and ZUS payment",
        "sufficient balance and ZUS payment with multiple transactions",
        "insufficient balance",
        "no ZUS payment",
    ]
    @pytest.mark.parametrize("history, balance, amount, expected_result, expected_balance", company_loan_tests, ids=ids)
    def test_company_loan(self, mock_requests_get, history, balance, amount, expected_result, expected_balance):
        company_account = CompanyAccount("Acme Corp", "1234567890")
        company_account.history = history
        company_account.balance = balance
        result = company_account.submit_for_loan(amount)
        assert result == expected_result
        assert company_account.balance == expected_balance
        
