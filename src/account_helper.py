from uuid import uuid4


class AccountHelper:

    @staticmethod
    def create_account_id() -> str:
        return str(uuid4())
