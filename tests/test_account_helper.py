from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.account_helper import AccountHelper


class TestAccountHelperCreationAccountId(TestCase):

    @patch('src.account_helper.uuid4')
    def test_return_generate_stringify_uuid(self, mock_uuid4):
        mock_uuid_1 = MagicMock()
        mock_uuid_1.__str__.return_value = 'uuid_1'
        mock_uuid_2 = MagicMock()
        mock_uuid_2.__str__.return_value = 'uuid_2'
        account_helper = AccountHelper()
        mock_uuid4.side_effect = [mock_uuid_1, mock_uuid_2]
        self.assertEqual('uuid_1', account_helper.create_account_id())
        self.assertEqual('uuid_2', account_helper.create_account_id())
