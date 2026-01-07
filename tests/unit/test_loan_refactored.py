from src.personal_account import PersonalAccount
import pytest

class TestAccount:
        
    @pytest.fixture(autouse=True)
    def create_account(self):
        self.account = PersonalAccount("John", "Doe", "89092909876")
        
    def test_3_positive_transfers(self):
        self.account.history = [100, 200, 500]
        result = self.account.submit_for_loan(300)
        assert result
        assert self.account.balance == 300
        
    def test_4_transfers_one_negative(self):
        self.account.history = [100, 200, 500, -100]
        result = self.account.submit_for_loan(300)
        assert not result
        assert self.account.balance == 0
        
    def test_large_positive_with_negatives(self):
        self.account.history = [-100, 20000, -100, 100, -1000]
        result = self.account.submit_for_loan(1500)
        assert result
        assert self.account.balance == 1500
        
    def test_single_small_positive(self):
        self.account.history = [100]
        result = self.account.submit_for_loan(500)
        assert not result
        assert self.account.balance == 0
        
    def test_multiple_transactions_with_large_negative(self):
        self.account.history = [-100, 100, 100, 100, -6000, 200]
        result = self.account.submit_for_loan(400)
        assert not result
        assert self.account.balance == 0
        
        
    @pytest.mark.parametrize("history, amount, expected_result, expected_balance", [
    ([100, 100, 100], 500, True, 500),
    ([-100, 100, -100, 100, 1000], 700, True, 700),
    ([-100, 20000, -100, 100, -1000], 1000, True, 1000),
    ([100], 666, False, 0),
    ([-100, 100, 100, 100, -6000, 200], 500, False , 0),
    ],
    ids=[
        "three small positives",
        "five transactions with two negatives",
        "large positive among negatives",
        "single small positive",
        "multiple transactions with large negative"
    ])
    def test_loan(self, history, amount, expected_result, expected_balance):
        self.account.history = history
        result = self.account.submit_for_loan(amount)
        assert result == expected_result
        assert self.account.balance == expected_balance
        