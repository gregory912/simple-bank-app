from database.model import company_details as cd
from database.model import profile as p
from database.model import bank_account as ba
from database.model import customer as c
from database.model import user as u
from database.repository import crud_repo as cr


class GenerateData:
    db_name = 'bank_app_test'
    db_port = '3308'
    company_details_repo = cr.CrudRepo(cd.CompanyDetails, db_name, db_port)
    profile_repo = cr.CrudRepo(p.Profile, db_name, db_port)
    bank_acc_repo = cr.CrudRepo(ba.BankAccount, db_name, db_port)
    user_repo = cr.CrudRepo(u.User, db_name, db_port)
    customer_repo = cr.CrudRepo(c.Customer, db_name, db_port)

    def check_data(self):
        """Check if data are already in the database"""
        return self.profile_repo.find_one(1)

    def generate_data(self):
        """Generate data for the test database in case the database is empty"""
        u_lastrow = self.user_repo.insert(u.User(
            login='login',
            password='1234',
            creation_date='2022-01-01 00:00:00'))
        c_lastrow = self.customer_repo.insert(c.Customer(
            id_user=u_lastrow,
            name='Name',
            surname='Surname',
            address='Address',
            email='email@gmail.com',
            phone='123456789',
            PESEL='123456789'))
        cd_lastrow = self.company_details_repo.insert(cd.CompanyDetails(
            company_name='Company',
            company_address='Company_address',
            NIP='123456789',
            REGON='123456789'))
        ba_lastrow = self.bank_acc_repo.insert(ba.BankAccount(
            bank_account_name='Example name',
            bank_account_number='123456789'))
        self.profile_repo.insert(p.Profile(
            id_customer=c_lastrow,
            id_account=ba_lastrow,
            id_company_account=cd_lastrow))

