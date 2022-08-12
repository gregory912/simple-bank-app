from dataclasses import dataclass


@dataclass
class CompanyDetails:
    id: int = None
    company_name: str = None
    company_address: str = None
    NIP: str = None
    REGON: str = None
