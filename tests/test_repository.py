import unittest
import os
from decimal import Decimal
from pathlib import Path

from src.account import Account
from src.repository import Repository


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.test_csv_file = Path('test_bank.csv')
        self.repository = Repository(self.test_csv_file)

    def tearDown(self):
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_save_state(self):
        accounts = {
            'account-1': Account('account-1', 'A', Decimal('1')),
            'account-2': Account('account-2', 'B', Decimal('2.2'))
        }
        self.repository.save_state(accounts)
        self.assertTrue(os.path.exists(self.test_csv_file))
        expected_csv_data = b'''account_id,name,balance
account-1,A,1
account-2,B,2.2
'''
        with open(self.test_csv_file, 'rb') as f:
            self.assertEqual(expected_csv_data, f.read())

    def test_load_state(self):
        # GIVEN a csv file is created with account data
        with open(self.test_csv_file, 'wb') as f:
            f.write(b'''account_id,name,balance
account-1,A,1
account-2,B,2.2
''')
        # WHEN state is loaded
        result = self.repository.load_state()

        # THEN a dict with account data is returned
        expected_data = {
            'account-1': Account('account-1', 'A', Decimal('1')),
            'account-2': Account('account-2', 'B', Decimal('2.2'))
        }
        self.assertEqual(result.keys(), expected_data.keys())
        for account_id, expected_account in expected_data.items():
            result_account = result[account_id]
            self.assertEqual(expected_account.account_id, result_account.account_id)
            self.assertEqual(expected_account.name, result_account.name)
            self.assertEqual(expected_account.balance, result_account.balance)

    def test_load_empty_state_if_csv_does_not_exist(self):
        self.assertDictEqual({}, self.repository.load_state())