import pytest

from src.company_account import CompanyAccount

class BaseClass:

    
    @pytest.fixture
    def set_up_mock(self, mocker, scope='function', autouse=True):
        mocker.patch.object(CompanyAccount, 'is_nip_active_in_MF_registry' , return_value=True)
        # pass