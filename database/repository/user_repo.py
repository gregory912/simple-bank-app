from mysql.connector import Error
from database.repository.crud_repo import CrudRepo
from database.model.user import User


class UserRepo(CrudRepo):
    def find_user(self, entity_login: str) -> User:
        """Find a user based on login"""
        try:
            find_one_row_sql = f"""select * from {self.__table_name__()} where login = "{entity_login}";"""
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_one_row_sql)
                result = cursor.fetchone()
                return self.__entity__(*result) if result else None
        except Error as err:
            print('Find user error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()
