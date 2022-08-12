from mysql.connector import Error
from mysql.connector import pooling
from typing import Type, List
import inflection


class CrudRepo:
    def __init__(self, entity_type: Type, db_name: str, db_port: str):
        self.__connection_pool__ = pooling.MySQLConnectionPool(
            pool_name='crud_repo_pool',
            pool_reset_session=True,
            host='localhost',
            user='user',
            database=db_name,
            password='user1234',
            port=db_port
        )
        self.__entity__ = entity_type
        self.__entity_type__ = type(entity_type())
        self.__create_tables__()

    def insert(self, entity) -> int:
        """Enter a row in the database"""
        try:
            insert_new_row_sql = f"""insert into {self.__table_name__()} {self.__column__names__for__insert__()} 
                                            values {self.__column_values_for_insert__(entity)}"""
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(insert_new_row_sql)
                connection_object.commit()
                return cursor.lastrowid
        except Error as err:
            print('Insert error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def insert_many(self, entities) -> List:
        """Enter multiple lines into the database"""
        try:
            values = ', '.join([f'{self.__column_values_for_insert__(e)}' for e in entities])
            insert_many_rows_sql = f"""insert into {self.__table_name__()} {self.__column__names__for__insert__()} 
                                            values {values}"""
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(insert_many_rows_sql)
                connection_object.commit()
                return [e.id for e in self.find_n_last(len(entities))]
        except Error as err:
            print('Insert many error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def update(self, entity_id, entity) -> int:
        """Update the row based on id"""
        try:
            update_row_sql = f"""update {self.__table_name__()} set {self.__column_names_and_values_for_update__(entity)} 
                                    where id = {entity_id};"""
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(update_row_sql)
                connection_object.commit()
                return entity_id
        except Error as err:
            print('Update error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def find_all(self) -> List:
        """Return all rows from the table"""
        try:
            find_all_rows_sql = f'select * from {self.__table_name__()}'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_all_rows_sql)
                return [self.__entity__(*row) for row in cursor.fetchall()]
        except Error as err:
            print('Find n last error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def find_one(self, entity_id):
        """Return one line based on id"""
        try:
            find_one_row_sql = f'select * from {self.__table_name__()} where id = {entity_id}'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_one_row_sql)
                result = cursor.fetchone()
                return self.__entity__(*result) if result else None
        except Error as err:
            print('Find n last error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def delete(self, entity_id) -> int:
        """Delete one row based on id"""
        try:
            delete_row_sql = f'delete from {self.__table_name__()} where id = {entity_id}'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(delete_row_sql)
                connection_object.commit()
                return entity_id
        except Error as err:
            print('Update error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def delete_all(self) -> list:
        """Delete all rows from the table"""
        try:
            deleted_entities = self.find_all()
            delete_row_sql = f'delete from {self.__table_name__()} where id >= 1'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(delete_row_sql)
                connection_object.commit()
                return deleted_entities
        except Error as err:
            print('Delete all error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def find_n_last(self, number) -> List:
        """Return recently added item"""
        try:
            find_n_rows_sql = f'select * from {self.__table_name__()} order by id desc limit {number}'
            connection_object = self.__connection_pool__.get_connection()
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                cursor.execute(find_n_rows_sql)
                return [self.__entity__(*row) for row in cursor.fetchall()]
        except Error as err:
            print('Find n last error section')
            print(err)
        finally:
            if connection_object.is_connected():
                cursor.close()
                connection_object.close()

    def __create_tables__(self):
        try:
            bank_account_sql = '''
                create table if not exists bank_accounts (
                    id integer primary key auto_increment,
                    bank_account_name varchar(30) not null,
                    bank_account_number varchar(30) not null,
                    balance decimal(6,1) default 0,
                    commision int default Null
                )
            '''

            user_sql = '''
                create table if not exists users (
                    id integer primary key auto_increment,
                    login varchar(50) not null unique,
                    password varchar(200) not null,
                    creation_date datetime
                )
            '''

            customer_sql = '''
                create table if not exists customers (
                    id integer primary key auto_increment,
                    id_user integer not null unique,
                    name varchar(20) not null,
                    surname varchar(20) not null,
                    address varchar(50) not null,
                    email varchar(20) not null unique,
                    phone varchar(15) not null,
                    PESEL varchar(15) not null unique,
                    foreign key (id_user) references users(id) on delete restrict on update cascade
                )
            '''

            company_detail_sql = '''
                create table if not exists company_details (
                    id integer primary key auto_increment,
                    company_name varchar(50) not null,
                    company_address varchar(50) not null,
                    NIP varchar(10) not null unique,
                    REGON varchar(15) not null unique
                )
            '''

            profile_sql = '''
                create table if not exists profiles (
                    id integer primary key auto_increment,
                    id_customer integer not null,
                    id_account integer not null,
                    id_company_account int default Null,
                    foreign key (id_customer) references customers(id) on delete restrict on update cascade,
                    foreign key (id_account) references bank_accounts(id) on delete restrict on update cascade,
                    foreign key (id_company_account) references company_details(id) on delete restrict on update cascade
                )
            '''

            transaction_sql = '''
                create table if not exists transactions (
                    id integer primary key auto_increment,
                    id_profile integer not null,
                    payment varchar(3),
                    payout varchar(3),
                    transaction_time datetime not null,
                    amount decimal(6,1) not null,
                    bank_account_number varchar(30),
                    recipient_name varchar(30),
                    transaction_name varchar(30) not null,
                    foreign key (id_profile) references profiles(id) on delete cascade on update cascade
                )
            '''

            connection = self.__connection_pool__.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(bank_account_sql)
                cursor.execute(user_sql)
                cursor.execute(customer_sql)
                cursor.execute(company_detail_sql)
                cursor.execute(profile_sql)
                cursor.execute(transaction_sql)
        except Error as err:
            print(err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def __table_name__(self) -> str:
        """Return a table name in a proper form"""
        return inflection.tableize(self.__entity_type__.__name__)

    def __field_names__(self) -> List:
        """Return the names of the member fields inside the class"""
        return list(self.__entity__().__dict__.keys())

    def __column__names__for__insert__(self) -> str:
        """Return the appropriate column names for use in INSERT"""
        return f"( {', '.join([field for field in self.__field_names__() if field.lower() != 'id'])} )"

    @staticmethod
    def __column_values_for_insert__(entity):
        """Return the appropriate values for use in INSERT"""
        def to_str(entry):
            return f"'{entry[1]}'" if isinstance(entry[1], (str, )) else str(entry[1])
        items_without_id = [x for x in entity.__dict__.items() if x[0].lower() != 'id']
        return f"( {', '.join([to_str(e) for e in items_without_id]).replace('None', 'Null')} )"

    @staticmethod
    def __column_names_and_values_for_update__(entity):
        """Return the appropriate values and column names for use in UPDATE"""
        def to_str(entry):
            return entry[0] + '=' + ("'" + entry[1] + "'" if isinstance(entry[1], str) else str(entry[1]))
        items_without_id = [x for x in entity.__dict__.items() if x[0].lower() != 'id']
        return f"{', '.join([to_str(e) for e in items_without_id])}"
