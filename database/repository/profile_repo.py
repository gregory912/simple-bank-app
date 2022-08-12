from mysql.connector import Error
from database.repository.crud_repo import CrudRepo


class ProfileRepo(CrudRepo):
    def get_all_accounts(self, entity_login) -> list:
        """Show all accounts for the entered user"""
        try:
            find_all_rows_sql = f"""SELECT  u.login, u.id, c.id, p.id, ba.bank_account_name, 
                                            ba.bank_account_number, ba.balance, 
                                            p.id_company_account, ba.commision, ba.id FROM users u
                                                JOIN customers c on u.id = c.id_user
                                                JOIN profiles p on c.id = p.id_customer
                                                JOIN bank_accounts ba on p.id_account = ba.id
                                                WHERE u.login = '{entity_login}';"""
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_all_rows_sql)
                return [row for row in cursor.fetchall()]
        except Error as err:
            print('Get all accounts error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()
