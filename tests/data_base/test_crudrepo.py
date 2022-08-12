import unittest
import random
from database.model import transaction as t
from .generate_data_for_tests import *
from decimal import Decimal
# python -m database.tests.test_crudrepo


class TestCrudRepo(unittest.TestCase):
    """The class checks individual methods in the CrudRepo Class"""
    db_name = 'bank_app_test'
    db_port = '3308'
    company_details_repo = cr.CrudRepo(cd.CompanyDetails, db_name, db_port)
    transaction_repo = cr.CrudRepo(t.Transaction, db_name, db_port)

    def setUp(self) -> None:
        generate_obj = GenerateData()
        if not generate_obj.check_data():
            generate_obj.generate_data()

    def test_insert_and_find_n_last(self):
        """The method checks the methods insert and find_n_last in the CrudRepo class"""
        entered_row = cd.CompanyDetails(company_name='Example Company Name',
                                        company_address='Example Adress',
                                        NIP=f"{self.draw_numbers(10)}",
                                        REGON=f"{self.draw_numbers(10)}")
        lastrow = self.company_details_repo.insert(entered_row)
        returned_row = self.company_details_repo.find_n_last(1)[0]
        entered_row.id = lastrow
        self.assertEqual(entered_row, returned_row, 'Methods insert and find_n_last return different values')

    def test_insert_and_find_one(self):
        """The method checks the methods insert and find_one in the CrudRepo class"""
        entered_row = cd.CompanyDetails(company_name='Example Company Name',
                                        company_address='Example Adress',
                                        NIP=f"{self.draw_numbers(10)}",
                                        REGON=f"{self.draw_numbers(10)}")
        lastrow = self.company_details_repo.insert(entered_row)
        returned_row = self.company_details_repo.find_one(lastrow)
        entered_row.id = lastrow
        self.assertEqual(entered_row, returned_row, 'Methods insert and find_one return different values')

    def test_update_and_find_one(self):
        """The method checks the methods update and find_one in the CrudRepo class"""
        row_to_update = cd.CompanyDetails(company_name='Example Company Name',
                                          company_address='Example Adress',
                                          NIP=f"{self.draw_numbers(10)}",
                                          REGON=f"{self.draw_numbers(10)}")
        row_to_update.id = self.company_details_repo.update(1, row_to_update)
        returned_row = self.company_details_repo.find_one(1)
        self.assertEqual(row_to_update, returned_row, 'Methods update and find_one return different values')

    def test_delete_all_insert_many_find_all(self):
        """The method checks the methods delete all, insert and find_all in the CrudRepo class"""
        # self.generate_data()
        lastrow = self.transaction_repo.insert(self.transaction_obj(1))
        self.transaction_repo.delete_all()
        list_of_transactions = []
        for x in range(10):
            lastrow += 1
            list_of_transactions.append(self.transaction_obj(lastrow))
        self.transaction_repo.insert_many(list_of_transactions)
        returned_rows = self.transaction_repo.find_all()
        for y in range(len(returned_rows)):
            returned_rows[y].transaction_time = returned_rows[y].transaction_time.strftime("%Y-%m-%d %H:%M:%S")
            returned_rows[y].amount = int(returned_rows[y].amount)
        self.assertEqual(list_of_transactions, returned_rows,
                         'Methods delete all, insert many and find all return different values')

    def test_insert_delete_find_one(self):
        """The method checks the methods insert, delete and find_one in the CrudRepo class"""
        lastrow = self.transaction_repo.insert(self.transaction_obj(1))
        self.transaction_repo.delete(lastrow)
        returned_row = self.transaction_repo.find_one(lastrow)
        self.assertEqual(returned_row, None, 'Methods insert, delete and find one return different values')

    @staticmethod
    def transaction_obj(id_: int):
        """Method returns transaction object"""
        return t.Transaction(id=id_,
                             id_profile=1,
                             payment=None,
                             payout='YES',
                             transaction_time='2022-01-01 00:00:00',
                             amount=Decimal('1000'),
                             bank_account_number='123456789',
                             recipient_name='Example Name',
                             transaction_name='Example Transaction Name')

    @staticmethod
    def draw_numbers(elements: int):
        """The method randomizes the numbers and returns a string"""
        return ''.join([str(random.randint(1, 9)) for _ in range(elements)])


if __name__ == '__main__':
    unittest.main()
