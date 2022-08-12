from dataclasses import dataclass


@dataclass
class Customer:
    id: int = None
    id_user: int = None
    name: str = None
    surname: str = None
    address: str = None
    email: str = None
    phone: str = None
    PESEL: str = None
