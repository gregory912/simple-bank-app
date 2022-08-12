from mysql.connector import Error
from database.repository.crud_repo import CrudRepo
from database.model.bank_account import BankAccount


class BankAccountRepo(CrudRepo):
    def check_if_account_exists(self, entity_account: str) -> BankAccount:
        """Check if the bank account exists for the entered bank account"""
        try:
            find_one_row_sql = f'select * from {self.__table_name__()} where bank_account_number = "{entity_account}";'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_one_row_sql)
                result = cursor.fetchone()
                return self.__entity__(*result) if result else None
        except Error as err:
            print('Check if user exists error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()
