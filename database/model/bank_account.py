from dataclasses import dataclass


@dataclass
class BankAccount:
    id: int = None
    bank_account_name: str = None
    bank_account_number: str = None
    balance: str = None
    commision: int = None
