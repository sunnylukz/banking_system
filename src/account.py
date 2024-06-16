from decimal import Decimal


class Account:
    def __init__(self, account_id: str, name: str, balance: Decimal):
        self.account_id = account_id
        self.name = name
        self.balance = balance

    @property
    def balance(self) -> Decimal:
        return self._balance

    @balance.setter
    def balance(self, value: Decimal):
        if value < 0:
            raise InvalidAccountOperationException('Insufficient balance')
        self._balance = value

    def deposit(self, amount: Decimal):
        self.balance += amount

    def withdraw(self, amount: Decimal):
        self.balance -= amount


class AccountNotFoundException(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id

    def __str__(self):
        return f'Unable to find account {self.account_id}'


class AccountIdExistsException(Exception):
    def __init__(self, account_id: str):
        self.account_id = account_id

    def __str__(self):
        return f'Account with account_id {self.account_id} already exists'


class InvalidAccountOperationException(Exception):
    pass