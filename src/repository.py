import logging
from decimal import Decimal
from pathlib import Path
from typing import Dict

import pandas as pd

from src.account import Account

logger = logging.getLogger(__name__)


class Repository:

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path

    def save_state(self, accounts: Dict[str, Account]):
        logger.info(f'Saving bank state to {self.csv_path}')
        data = [{'account_id': account.account_id, 'name': account.name, 'balance': str(account.balance)}
                for account in accounts.values()]
        pd.DataFrame.from_records(data).to_csv(self.csv_path, index=False)

    def load_state(self) -> Dict[str, Account]:
        if self.csv_path.is_file():
            print(f'Loading state from {self.csv_path}')
            state_df = pd.read_csv(self.csv_path, converters={'account_id': str,
                                                              'balance': str})
            return {
                account['account_id']: Account(account_id=account['account_id'],
                                               name=account['name'],
                                               balance=Decimal(account['balance']))
                for account in state_df.to_dict(orient='records')
            }
        else:
            print(f'Unable to find state init file from {self.csv_path}, start a fresh state')
            return dict()
