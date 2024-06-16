# Simple Banking System

The is a command-line interface that allows users to interact with the simple banking system. It provides various commands to create accounts, perform deposits, withdrawals, transfers between accounts, and save bank's state to a csv.

## Installation

1. Clone the repository or download the source code.
2. Install the necessary dependencies. (Ensure you have Python installed, tested python version 3.9.6)

## Usage

To use the Banking System CLI, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the root directory of the repository.
3. Run the following command:

```bash
python main.py -f <PATH TO STATE CSV FILE>
```
Replace <PATH TO STATE CSV FILE> with the desired path of the state file to save and load the bank's state.

After the execution of the command, an interactive CLI will be opened

```commandline
✗ python main.py -f example_state.csv
Unable to find state init file from example_state.csv, start a fresh state
Welcome to the Banking CLI!
Available commands:
- create_account
        Parameters (in order): name, balance
        Usage: Create a new account
- deposit
        Parameters (in order): account_id, amount
        Usage: Deposit into an account
- withdraw
        Parameters (in order): account_id, amount
        Usage: Withdraw from an account
- transfer
        Parameters (in order): from_account_id, to_account_id, amount
        Usage: Transfer between accounts
- save_state
        Parameters (in order): 
        Usage: Save bank state to a csv file
- exit
        Parameters (in order): 
        Usage: Exit the program

Enter a command: create_account Adam 1234.5
Created new account: <Account account_id=da5dcff7-4606-4875-bb58-f0dcbf4cfe92, name=Adam, balance=1234.5>

Enter a command: create_account Troy 0
Created new account: <Account account_id=98386356-35e6-402f-9aa0-02ac58874d87, name=Troy, balance=0>

Enter a command: withdraw 98386356-35e6-402f-9aa0-02ac58874d87 10
Insufficient balance

Enter a command: withdraw da5dcff7-4606-4875-bb58-f0dcbf4cfe92 10            
Withdrawn 10 from account da5dcff7-4606-4875-bb58-f0dcbf4cfe92
Account state after withdrawal: <Account account_id=da5dcff7-4606-4875-bb58-f0dcbf4cfe92, name=Adam, balance=1224.5>

Enter a command: deposit 98386356-35e6-402f-9aa0-02ac58874d87 30.5
Deposited 30.5 to account 98386356-35e6-402f-9aa0-02ac58874d87
Account state after deposit: <Account account_id=98386356-35e6-402f-9aa0-02ac58874d87, name=Troy, balance=30.5>

Enter a command: transfer da5dcff7-4606-4875-bb58-f0dcbf4cfe92 98386356-35e6-402f-9aa0-02ac58874d87 150
Transferred 150 from account da5dcff7-4606-4875-bb58-f0dcbf4cfe92 to account 98386356-35e6-402f-9aa0-02ac58874d87
From account state after transfer: <Account account_id=da5dcff7-4606-4875-bb58-f0dcbf4cfe92, name=Adam, balance=1074.5>
To account state after transfer: <Account account_id=98386356-35e6-402f-9aa0-02ac58874d87, name=Troy, balance=180.5>

Enter a command: save_state
Saved current bank state

Enter a command: exit
Exiting the program...

```

You will find an exported state in `example.csv`

```commandline
✗ cat example_state.csv 
account_id,name,balance
da5dcff7-4606-4875-bb58-f0dcbf4cfe92,Adam,1074.5
98386356-35e6-402f-9aa0-02ac58874d87,Troy,180.5
```

## Assumption
1. Account name will only have 1 word
2. Account cannot be overdrafted
3. If state csv file exists, it will be automatically loaded when program starts
