from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Transaction:
    id: int = None
    id_profile: int = None
    payment: str = None
    payout: str = None
    transaction_time: str = None
    amount: Decimal = None
    bank_account_number: str = None
    recipient_name: str = None
    transaction_name: str = None
