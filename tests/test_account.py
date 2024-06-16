from decimal import Decimal
from unittest import TestCase

from src.account import Account, InvalidAccountOperationException


class TestAccount(TestCase):
    def test_account_creation(self):
        account = Account(account_id='account-1', name='Tom', balance=Decimal('123.4'))
        self.assertEqual('account-1', account.account_id)
        self.assertEqual('Tom', account.name)
        self.assertEqual(Decimal('123.4'), account.balance)

    def test_raise_invalid_account_operation_with_balance_is_set_to_smaller_than_zero(self):
        account = Account(account_id='account-1', name='Tom', balance=Decimal('123.4'))

        with self.assertRaises(InvalidAccountOperationException):
            account.balance = Decimal('-0.001')
        self.assertEqual(Decimal('123.4'), account.balance)

    def test_deposit_to_account(self):
        account = Account(account_id='account-1', name='Tom', balance=Decimal('123.4'))
        account.deposit(Decimal('1.1'))
        self.assertEqual(Decimal('124.5'), account.balance)

    def test_withdraw(self):
        account = Account(account_id='account-1', name='Tom', balance=Decimal('123.4'))
        account.withdraw(Decimal('1.1'))
        self.assertEqual(Decimal('122.3'), account.balance)

    def test_raise_invalid_account_operation_with_overdraft(self):
        account = Account(account_id='account-1', name='Tom', balance=Decimal('123.4'))
        with self.assertRaises(InvalidAccountOperationException):
            account.withdraw(Decimal('123.5'))
        self.assertEqual(Decimal('123.4'), account.balance)
