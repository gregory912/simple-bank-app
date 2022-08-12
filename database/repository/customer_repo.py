from mysql.connector import Error
from database.repository.crud_repo import CrudRepo
from database.model.customer import Customer


class CustomerRepo(CrudRepo):
    def get_customer_id(self, entity_id: int) -> Customer:
        """Get the client id based on the user id"""
        try:
            find_one_row_sql = f'select * from {self.__table_name__()} where id_user = {entity_id};'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_one_row_sql)
                result = cursor.fetchone()
                return self.__entity__(*result) if result else None
        except Error as err:
            print('Check get customer id error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()
