from database.model.user import User
from database.model.customer import Customer
from database.model.profile import Profile
from database.model.bank_account import BankAccount
from database.model.company_details import CompanyDetails
from database.model.transaction import Transaction
from database.repository.crud_repo import CrudRepo
from database.repository.user_repo import UserRepo
from database.repository.profile_repo import ProfileRepo
from database.repository.bank_account_repo import BankAccountRepo
from database.repository.customer_repo import CustomerRepo
from database.repository.transaction_repo import TransactionRepo
from database.repository.company_details_repo import CompanyDetailsRepo
from .security.security import Security
from datetime import date, datetime, timedelta
from decimal import Decimal


class UserActions:
    db_name = 'bank_app'
    db_port = '3307'
    user_repo = CrudRepo(User, db_name, db_port)

    def insert_customer(
            self, id_user: int, name: str, surname: str, address: str, email: str, phone: str, pesel: str) -> int:
        """Insert customer data into the database"""
        return CrudRepo(Customer, self.db_name, self.db_port).insert(Customer(
            id_user=id_user,
            name=name,
            surname=surname,
            address=address,
            email=email,
            phone=phone,
            PESEL=pesel))

    def insert_user(self, login: str, password: str) -> int:
        """Insert user data to users table. Return lastrow"""
        return CrudRepo(User, self.db_name, self.db_port).insert(User(
            login=login,
            password=password,
            creation_date=self.get_time()))

    def insert_bank_account(self, acc_name: str, acc_num: str, balance: str = '0', commision: int = 0) -> int:
        """Insert bank account data to bank accounts table. Return lastrow"""
        return CrudRepo(BankAccount, self.db_name, self.db_port).insert(BankAccount(
            bank_account_name=acc_name,
            bank_account_number=acc_num,
            balance=balance,
            commision=commision))

    def insert_company_detail(self, name: str, address: str, nip: str, regon: str) -> int:
        """Insert company detail data to company details table. Return lastrow"""
        return CrudRepo(CompanyDetails, self.db_name, self.db_port).insert(CompanyDetails(
            company_name=name,
            company_address=address,
            NIP=nip,
            REGON=regon))

    def insert_profile(self, id_customer: int, id_account: int, company_account: int = None) -> int:
        """Insert profile data to company profiles table. Return lastrow"""
        return CrudRepo(Profile, self.db_name, self.db_port).insert(Profile(
            id_customer=id_customer,
            id_account=id_account,
            id_company_account=company_account))

    def insert_transaction(
            self, id_profile: int, payment: str, payout: str,
            amount: Decimal, bank_account_number: str, recipient_name: str, transaction_name: str) -> int:
        """Insert transaction data to company transactions table. Return lastrow"""
        return CrudRepo(Transaction, self.db_name, self.db_port).insert(Transaction(
            id_profile=id_profile,
            payment=payment,
            payout=payout,
            transaction_time=self.get_time(),
            amount=amount,
            bank_account_number=bank_account_number,
            recipient_name=recipient_name,
            transaction_name=transaction_name
        ))

    def update_bank_account(self, id_: int, bank_account_name: str, bank_account_number: str,
                            balance: str, commision: int) -> int:
        """Update bank_accounts table based on entered id."""
        return CrudRepo(BankAccount, self.db_name, self.db_port).update(id_, BankAccount(
            id=id_,
            bank_account_name=bank_account_name,
            bank_account_number=bank_account_number,
            balance=balance,
            commision=commision))

    def check_user(self, login: str) -> User:
        """Check if user with entered login exists"""
        return UserRepo(User, self.db_name, self.db_port).find_user(login)

    def check_bank_account(self, bank_account: str) -> BankAccount:
        """Check if entered bank account exist in data base"""
        return BankAccountRepo(BankAccount, self.db_name, self.db_port).check_if_account_exists(bank_account)

    def check_nip(self, nip: str) -> CompanyDetails:
        """Check if entered nip number exist in data base"""
        return CompanyDetailsRepo(CompanyDetails, self.db_name, self.db_port).check_if_nip_exists(nip)

    def find_user(self, login: str, password: str) -> User:
        """Find user based on login and password"""
        user_data = UserRepo(User, self.db_name, self.db_port).find_user(login)
        if Security.check_password(password, user_data.password):
            return user_data

    def get_all_accounts(self, login: str) -> list:
        """Get all accounts which belongs to the entered user"""
        return ProfileRepo(Profile, self.db_name, self.db_port).get_all_accounts(login)

    def get_customer_id(self, user_id: int) -> Customer:
        """Get customer id for logged user"""
        return CustomerRepo(Customer, self.db_name, self.db_port).get_customer_id(user_id)

    def get_transactions_betwn_dates(self, today_date: date, account: int) -> list:
        """Return all transactions between dates"""
        return TransactionRepo(Transaction, self.db_name, self.db_port).get_records_between_dates(
            self.get_first_day(today_date),
            self.get_last_day(today_date),
            account)

    def get_trans_for_user(self, login: str) -> list:
        """Get all records transactions for the user"""
        return TransactionRepo(Transaction, self.db_name, self.db_port).get_transactions_for_user(login)

    @staticmethod
    def get_time() -> str:
        """Get date and time without seconds"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_first_day(date_: datetime.date) -> str:
        """Get first day of indicated date"""
        year = str(date_)[:4]
        month = str(date_)[5:7]
        return year + '-' + month + '-' + '01'

    @staticmethod
    def get_last_day(date_: datetime.date) -> str:
        """Return the date on the last day of the month"""
        month = date_.month
        while True:
            date_ = date_ + timedelta(days=1)
            if month != date_.month:
                return date_ - timedelta(days=1)
