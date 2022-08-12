from mysql.connector import Error
from database.repository.crud_repo import CrudRepo
from database.model.company_details import CompanyDetails


class CompanyDetailsRepo(CrudRepo):
    def check_if_nip_exists(self, entity_nip: str) -> CompanyDetails:
        """Check if NIP number provided has not already been used for another account"""
        try:
            find_one_row_sql = f'select * from {self.__table_name__()} where NIP = {entity_nip}'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_one_row_sql)
                result = cursor.fetchone()
                return self.__entity__(*result) if result else None
        except Error as err:
            print('Check if NIP exists error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()
