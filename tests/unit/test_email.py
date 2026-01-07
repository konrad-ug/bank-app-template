import datetime
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestEmail:
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    email_address = "test@email.com"
    
    def test_send_history_via_email_personal_account(self, mocker):
        account = PersonalAccount("Jane", "Smith", "98765432101")
        # account.incoming_transfer(150.0)
        # account.outgoing_transfer(50.0)
        account.history = [150.0, -50.0]
        mock_send = mocker.patch('src.account.SMTPClient.send')
        mock_send.return_value = True
        
        result = account.send_history_via_email(self.email_address)
        
        assert result is True
        
        mock_send.assert_called_once_with("Account Transfer History " + self.today_date, 
                                          "Personal account history:" + account.history.__str__(), 
                                          self.email_address)
       
        
    def test_send_history_via_email_personal_account_failed(self, mocker):
        account = PersonalAccount("Jane", "Smith", "98765432101")
        account.history = [150.0, -50.0]
        
        mock_send = mocker.patch('src.account.SMTPClient.send', return_value=False)
        
        result = account.send_history_via_email(self.email_address)
        
        assert result is False

