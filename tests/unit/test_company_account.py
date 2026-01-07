from pytest_mock import MockFixture
from src.company_account import CompanyAccount
import pytest
from base_class import BaseClass as base_class

class TestCompanyAccount(base_class):
    
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker: MockFixture):
        mocker.patch.object(CompanyAccount, 'is_nip_active_in_MF_registry', return_value=True)
    
    def test_company_account_creation(self):
        # mocker.patch.object(CompanyAccount, 'is_nip_active_in_MF_registry', return_value=True)
        # mock = mocker.patch('requests.get')
        # mock.return_value.status_code = 200
        # mock.return_value.json.return_value = {"result": {"subject": {"statusVat": "nieCzynny"}}}
        company_account = CompanyAccount("Tech Solutions", "8461627563")
        assert company_account.name == "Tech Solutions"
        assert company_account.balance == 0.0
        assert company_account.nip == "8461627563"
        
    # def test_throw_error(self):
    #     mocker = MockFixture()
    #     mock = mocker.patch('requests.get')
    #     mock.return_value.status_code = 200
    #     mock.return_value.json.return_value = {"result": {"subject": {"statusVat": "nieCzynny"}}}        
    #     try:
    #         company_account = CompanyAccount("Tech Solutions", "8461627563")
    #         assert False, "ValueError was not raised"
    #     except ValueError as e:
    #         assert str(e) == "NIP is not active in MF registry"
        
    def test_nip_too_long(self):
        company_account = CompanyAccount("Business Corp", "1234567890123")
        assert company_account.nip == "Invalid"
        
    def test_nip_too_short(self):
        company_account = CompanyAccount("Business Corp", "12345")
        assert company_account.nip == "Invalid"
        
    def test_nip_none(self):
        company_account = CompanyAccount("Business Corp", None)
        assert company_account.nip == "Invalid"
        
    def test_nip_with_non_digit_characters(self):
        company_account = CompanyAccount("Business Corp", "12345A7890")
        assert company_account.nip == "Invalid"