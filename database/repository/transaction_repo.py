from mysql.connector import Error
from database.repository.crud_repo import CrudRepo


class TransactionRepo(CrudRepo):
    def get_records_between_dates(self, starting_date: str, end_date: str, account: int) -> list:
        """Get transactions between entered dates"""
        try:
            find_all_rows_sql = f"""
            SELECT * FROM transactions
                JOIN profiles p on transactions.id_profile = p.id
                WHERE transaction_time 
                BETWEEN '{starting_date} 00:00:00' AND '{end_date} 23:59:59' AND p.id_account = {account};"""
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_all_rows_sql)
                return [row for row in cursor.fetchall()]
        except Error as err:
            print('Get records between dates error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def get_transactions_for_user(self, entity_login: str) -> list:
        """Get transactions for entered user"""
        try:
            find_all_rows_sql = f"""
            select t.*  from transactions t
                JOIN profiles p on t.id_profile = p.id
                JOIN customers c on p.id_customer = c.id
                JOIN users u on c.id_user = u.id
                where u.login = '{entity_login}';
            """
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_all_rows_sql)
                return [self.__entity__(*row) for row in cursor.fetchall()]
        except Error as err:
            print('Get transactions for user error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()
