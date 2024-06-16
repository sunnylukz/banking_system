from argparse import ArgumentParser
from pathlib import Path

from decimal import Decimal, InvalidOperation
from src.account_helper import AccountHelper
from src.bank import Bank
from src.exception import BankException
from src.repository import Repository


parser = ArgumentParser()
parser.add_argument('-f', dest='csv_path', help='Path of state csv file to be loaded from and saved to', required=True)
init_args = parser.parse_args()
csv_path = init_args.csv_path


# Create an instance of the BankingSystem
bank = Bank(account_helper=AccountHelper(),
            repository=Repository(csv_path=Path(csv_path)))

# Define the available commands and their arguments
commands = {
    'create_account': {
        'args': ['name', 'balance'],
        'help': 'Create a new account',
        'numeric_args': ['balance']
    },
    'deposit': {
        'args': ['account_id', 'amount'],
        'help': 'Deposit into an account',
        'numeric_args': ['amount']
    },
    'withdraw': {
        'args': ['account_id', 'amount'],
        'help': 'Withdraw from an account',
        'numeric_args': ['amount']
    },
    'transfer': {
        'args': ['from_account_id', 'to_account_id', 'amount'],
        'help': 'Transfer between accounts',
        'numeric_args': ['amount']
    },
    'save_state': {
        'args': [],
        'help': 'Save bank state to a csv file',
    },
    'exit': {
        'args': [],
        'help': 'Exit the program',
    },
}


# Print the available commands and their usage
def print_command_usage():
    print('Available commands:')
    for command, details in commands.items():
        args = ', '.join(details['args'])
        print(f'- {command}\n\tParameters (in order): {args}\n\tUsage: {details["help"]}')
    print()


# Process the user's input
def process_input(user_input):
    parts = user_input.split()
    command = parts[0]
    args = parts[1:]

    if command == 'exit':
        print('Exiting the program...')
        return False

    if command not in commands:
        print('Invalid command. Please try again.')
        return True

    if len(args) != len(commands[command]['args']):
        print('Invalid number of arguments. Please try again.')
        return True

    command_args = {}
    for i, arg in enumerate(commands[command]['args']):
        if arg in commands[command]['numeric_args']:
            try:
                args[i] = Decimal(args[i])
            except InvalidOperation:
                print(f'{arg} should be in numerical format. Please try again.')
        command_args[arg] = args[i]

    if command == 'create_account':
        account = bank.create_account(
            name=command_args['name'],
            balance=Decimal(command_args.get('balance', 0)),
        )
        print(f'Created new account: {account}')
    elif command == 'deposit':
        account = bank.deposit(account_id=command_args['account_id'],
                               amount=command_args['amount'])
        print(f'Deposited {command_args["amount"]} to account {command_args["account_id"]}')
        print(f'Account state after deposit: {account}')
    elif command == 'withdraw':
        account = bank.withdraw(account_id=command_args['account_id'],
                                amount=command_args['amount'])
        print(f'Withdrawn {command_args["amount"]} from account {command_args["account_id"]}')
        print(f'Account state after withdrawal: {account}')
    elif command == 'transfer':
        from_account, to_account = bank.transfer(from_account_id=command_args['from_account_id'],
                                                 to_account_id=command_args['to_account_id'],
                                                 amount=Decimal(command_args['amount']))
        print(f'Transferred {command_args["amount"]} from account {command_args["from_account_id"]} '
              f'to account {command_args["to_account_id"]}')
        print(f'From account state after transfer: {from_account}')
        print(f'To account state after transfer: {to_account}')
    elif command == 'save_state':
        bank.save_state()
        print(f'Saved current bank state')
    print()
    return True


# Run the interactive CLI
print('Welcome to the Banking CLI!')
print_command_usage()

running = True
while running:
    user_input = input('Enter a command: ')
    try:
        running = process_input(user_input)
    except BankException as e:
        # print business exception and continue application
        print(e)
        print()

