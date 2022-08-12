import unittest
from database.model import company_details as cd
from database.model import user as u
from database.repository import user_repo as ur
from database.repository import company_details_repo as cdr
import random


class TestAdditionalRepos(unittest.TestCase):
    """The class checks individual methods in the Additional Repos Class"""
    db_name = 'bank_app_test'
    db_port = '3308'
    user_repo = ur.UserRepo(u.User, db_name, db_port)
    company_repo = cdr.CompanyDetailsRepo(cd.CompanyDetails, db_name, db_port)

    def test_insert_and_check_if_user_exists(self):
        """The method checks the methods insert from CrudRepo Class,
            and check_if_user_exists from UserRepo Class"""
        login = self.generate_login()
        entered_row = u.User(login=login,
                             password='123456789',
                             creation_date='2022-01-01 00:00:00')
        lastrow = self.user_repo.insert(entered_row)
        entered_row.id = lastrow
        returned_row = self.user_repo.find_user(login)
        returned_row.creation_date = returned_row.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(entered_row, returned_row,
                         'Methods insert and check_if_user_exists return different values')

    def test_insert_and_find_user(self):
        """The method checks the methods insert from CrudRepo Class,
            and find user from UserRepo Class"""
        login = self.generate_login()
        entered_row = u.User(login=login,
                             password='123456789',
                             creation_date='2022-01-01 00:00:00')
        lastrow = self.user_repo.insert(entered_row)
        entered_row.id = lastrow
        returned_row = self.user_repo.find_user(login)
        returned_row.creation_date = returned_row.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(entered_row, returned_row,
                         'Methods insert and find user return different values')

    def test_insert_and_check_if_nip_exists(self):
        """The method checks the methods insert from CrudRepo Class,
            and find user from UserRepo Class"""
        nip = self.draw_numbers(10)
        entered_row = cd.CompanyDetails(company_name='Example Company Name',
                                        company_address='Example Adress',
                                        NIP=nip,
                                        REGON=f"{self.draw_numbers(10)}")
        lastrow = self.company_repo.insert(entered_row)
        entered_row.id = lastrow
        returned_row = self.company_repo.check_if_nip_exists(nip)
        self.assertEqual(entered_row, returned_row,
                         'Methods insert and check_if_nip_exists return different values')

    @staticmethod
    def generate_login():
        """The method randomizes the letters and returns a string"""
        return ''.join([chr(random.randint(65, 90)) for _ in range(10)])

    @staticmethod
    def draw_numbers(elements: int):
        """The method randomizes the numbers and returns a string"""
        return ''.join([str(random.randint(1, 9)) for x in range(elements)])


if __name__ == '__main__':
    unittest.main()
