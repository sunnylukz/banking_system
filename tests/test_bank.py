from decimal import Decimal
from unittest import TestCase
from unittest.mock import create_autospec

from src.account import Account, AccountNotFoundException, AccountIdExistsException, InvalidAccountOperationException
from src.account_helper import AccountHelper
from src.bank import Bank
from src.repository import Repository


class BaseBankTestCase(TestCase):
    __test__ = False

    def setUp(self, ) -> None:
        self.mock_account_helper = create_autospec(AccountHelper)
        self.mock_repository = create_autospec(Repository)
        self.mock_repository.load_state.return_value = {}  # Assume bank starts with fresh state
        self.bank = Bank(account_helper=self.mock_account_helper,
                         repository=self.mock_repository)


class TestBankCreateAccount(BaseBankTestCase):
    __test__ = True

    def test_create_account(self):
        # GIVEN a bank is set up
        mock_account_id = 'mock-account-id'
        self.mock_account_helper.create_account_id.return_value = mock_account_id
        account_name = 'Tom'
        account_initial_balance = Decimal('1234.56')

        # WHEN account is created
        account = self.bank.create_account(account_name, account_initial_balance)

        # THEN created account has correct information
        self.assertEqual(mock_account_id, account.account_id, 'Account id should be equal to returned value from '
                                                              'helper class')
        self.assertEqual(account_initial_balance, account.balance, 'Account balance should equal to initial balance')
        self.assertEqual(account_name, account.name, 'Account name should equal to provided name')

    def test_if_balance_is_not_provided_then_account_default_balance_is_zero(self):
        # GIVEN a bank is set up
        mock_account_id = 'mock-account-id'
        self.mock_account_helper.create_account_id.return_value = mock_account_id
        account_name = 'Tom'

        # WHEN account is created without initial balance
        account = self.bank.create_account(account_name)

        # THEN created account has 0 balance
        self.assertEqual(Decimal('0'), account.balance, 'Default account balance should be zero')

    def test_raise_account_id_exists_exception_if_account_id_already_exists(self):
        # GIVEN a bank is set up
        self.mock_account_helper.create_account_id.side_effect = ['mock-account-id', 'mock-account-id']

        # WHEN accounts are created the same account id
        # THEN AccountIdExistsException is thrown
        with self.assertRaises(AccountIdExistsException):
            self.bank.create_account('Tom')
            self.bank.create_account('David')


class TestBankGetAccount(BaseBankTestCase):
    __test__ = True

    def test_get_existing_account(self):
        # Given an account is created
        self.mock_account_helper.create_account_id.return_value = 'mock-account-id'
        account = self.bank.create_account('Tom')

        # When the account is retrieved
        retrieved_account = self.bank.get_account(account.account_id)

        # Then the retrieved account should have the same account information
        self.assertEqual(account.account_id, retrieved_account.account_id)
        self.assertEqual(account.name, retrieved_account.name)
        self.assertEqual(account.balance, retrieved_account.balance)

    def test_raise_account_not_found_exception_when_get_non_existent_account(self):
        # Given an account is not created
        # When the account is retrieved
        # Then AccountNotFound should be raised
        with self.assertRaises(AccountNotFoundException):
            self.bank.get_account('some-account-id')


class TestBankDeposit(BaseBankTestCase):
    __test__ = True

    def test_deposit(self):
        # GIVEN an account is created
        account = self.bank.create_account('Andy', Decimal('100.1'))

        # WHEN there is a deposit
        self.bank.deposit(account.account_id, Decimal('11.01'))

        # THEN account's balance is increased by the deposited amount
        self.assertEqual(Decimal('111.11'), account.balance)


class TestBankWithdraw(BaseBankTestCase):
    __test__ = True

    def test_withdraw(self):
        # GIVEN an account is created
        account = self.bank.create_account('Andy', Decimal('100.1'))

        # WHEN there is a withdrawal
        self.bank.withdraw(account.account_id, Decimal('10.1'))

        # THEN account's balance is increased by the deposited amount
        self.assertEqual(Decimal('90'), account.balance)

    def test_raise_invalid_account_operation_exception_when_an_overdraft_occurs(self):
        # GIVEN an account is created
        account = self.bank.create_account('Andy', Decimal('100.1'))

        # WHEN there is a withdrawal with amount larger than balance
        # THEN an invalid account operation exception is raised
        with self.assertRaises(InvalidAccountOperationException):
            self.bank.withdraw(account.account_id, Decimal('100.2'))

        # AND the account balance remains the same
        self.assertEqual(Decimal('100.1'), account.balance)


class TestBankTransfer(BaseBankTestCase):
    __test__ = True

    def setUp(self) -> None:
        super().setUp()
        self.mock_account_helper.create_account_id.side_effect = [
            'mock-account-1',
            'mock-account-2'
        ]

    def test_transfer(self):
        # GIVEN an account is created
        from_account = self.bank.create_account('Andy', Decimal('100.1'))
        to_account = self.bank.create_account('Tom', Decimal('1'))

        # WHEN there is a transfer without overdraft
        self.bank.transfer(from_account_id=from_account.account_id,
                           to_account_id=to_account.account_id,
                           amount=Decimal('10.1'))

        # THEN from account's balance is decreased by the transferred amount
        self.assertEqual(Decimal('90'), from_account.balance)
        # AND to account's balance is increased by the transferred amount
        self.assertEqual(Decimal('11.1'), to_account.balance)

    def test_raise_invalid_account_operation_exception_when_an_overdraft(self):
        # GIVEN an account is created
        from_account = self.bank.create_account('Andy', Decimal('100.1'))
        to_account = self.bank.create_account('Tom', Decimal('1'))

        # WHEN there is a withdrawal with amount larger than from account's balance
        # THEN an invalid account operation exception is raised
        with self.assertRaises(InvalidAccountOperationException):
            self.bank.transfer(from_account_id=from_account.account_id,
                               to_account_id=to_account.account_id,
                               amount=Decimal('100.2'))

        # AND both accounts' balances remain the same
        self.assertEqual(Decimal('100.1'), from_account.balance)
        self.assertEqual(Decimal('1'), to_account.balance)


class TestBankLoadState(BaseBankTestCase):
    __test__ = True

    def test_populate_bank_accounts(self):
        state = {
            'account-1': Account('account-1', 'Tom', Decimal('1000')),
            'account-2': Account('account-2', 'May', Decimal('2000'))
        }
        self.mock_repository.load_state.return_value = state
        self.bank.load_state()
        self.assertDictEqual(state, self.bank.accounts)


class TestBankSaveState(BaseBankTestCase):
    __test__ = True

    def test_call_repository_save_state_with_bank_state(self):
        state = {
            'account-1': Account('account-1', 'Tom', Decimal('1000')),
            'account-2': Account('account-2', 'May', Decimal('2000'))
        }
        self.bank.accounts = state
        self.bank.save_state()
        self.mock_repository.save_state.assert_called_once_with(state)
