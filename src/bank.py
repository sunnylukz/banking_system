import logging
from decimal import Decimal
from typing import Tuple

from src.account import Account, AccountIdExistsException, AccountNotFoundException
from src.account_helper import AccountHelper
from src.repository import Repository

logger = logging.getLogger(__name__)


class Bank:
    def __init__(self,
                 account_helper: AccountHelper,
                 repository: Repository):
        self.account_helper = account_helper
        self.repository = repository
        self.accounts = self.repository.load_state()

    def create_account(self, name: str, balance: Decimal = Decimal('0')) -> Account:
        account_id = self.account_helper.create_account_id()

        if account_id in self.accounts:
            raise AccountIdExistsException(account_id)

        account = Account(account_id=account_id,
                          name=name,
                          balance=balance)
        self.accounts[account_id] = account
        logger.info(f'Created a new account for {name} (account_id: {account_id}) '
                    f'with a balance {balance}')
        return account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise AccountNotFoundException(account_id)
        return self.accounts[account_id]

    def deposit(self, account_id: str, amount: Decimal) -> Account:
        account = self.get_account(account_id)
        account.deposit(amount)
        return account

    def withdraw(self, account_id: str, amount: Decimal) -> Account:
        account = self.get_account(account_id)
        account.withdraw(amount)
        return account

    def transfer(self, from_account_id: str, to_account_id: str, amount: Decimal) -> Tuple[Account, Account]:
        # Assumption: This application is not used with concurrency
        from_account = self.withdraw(from_account_id, amount)
        to_account = self.deposit(to_account_id, amount)
        return from_account, to_account

    def save_state(self):
        self.repository.save_state(self.accounts)

    def load_state(self):
        self.accounts = self.repository.load_state()
