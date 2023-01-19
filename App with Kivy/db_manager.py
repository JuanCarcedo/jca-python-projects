"""
    Date: 09/01/2023
    Modified/updated from db_manager; bookstore project in my GitHub:
    https://github.com/JuanCarcedo/jca-python-projects/tree/main/Bookstore
    Class to manage the database interaction.
    :copyright: (c) 2023 Juan Carcedo.
    :licence: MIT, see LICENSE.txt for further details.

    NOTE: Remember to update the PATH_DB if you want to change the db.
"""
import sqlite3
from tabulate import tabulate  # Pretty tables


class DataBase:
    """
    Class to handle all items required with iterations with DB.
    """
    PATH_DB = 'data/appdata.db'

    def __init__(self, path_to_db: str = PATH_DB):
        """
        Constructor of the class. Note: path to db is required.
        :param path_to_db: File to be created.
        """
        # Define private variables. The class will handle internally each request.
        # Connection to the db.
        self.__db = sqlite3.connect(path_to_db)
        self.__cursor = self.__db.cursor()

    def create_table(self, table_name: str, table_fields: str) -> None:
        """
        Create a new table. Name and fields for table must be correct.
        :param table_name: Name of the table.
        :param table_fields: Fields for the table.
        :return: None.
        """
        # Generate the SQL code for the table:
        try:
            # try-except block to prevent issues if the table is already there.
            sql_code = f'''
                CREATE TABLE {table_name} ({table_fields})'''
            # Get data into db and commit the change:
            self.__cursor.execute(sql_code)
            self.__db.commit()

        except sqlite3.OperationalError:
            # Catch the error if the table already exists.
            # Will do nothing.
            pass

        except Exception as error:
            # Catch other errors.
            # Rollback any wrong changes.
            self.__db.rollback()
            raise error

        else:
            # Only if all goes well.
            pass

    def insert_records(self,
                       data,
                       table_header: list,
                       table_name: str,
                       method: str = 'multiple',
                       key_auto: bool = False) -> None:
        """
        INSERT records in the database. Can insert one record or multiple ones using method.
        :param data: Data to insert into database (must be tuple for single insertion or
                    list of tuples for multiple insertion).
        :param table_header: Header of the table in List format.
        :param table_name: Name of table for inserting.
        :param method: 'single' for single insert, 'multiple' for multiple inserts.
        :param key_auto: If key in table is set as autoincrement, set to True.
        :return: None.
        """
        # Add data into the new table.
        print(f'+-- Adding {method} records into table "{table_name}".')

        try:
            # try-except to catch issues whilst updating the db.
            number_fields = len(table_header) - 1  # Reduced by 1 because one ? will be added manually.
            # Note: The length of the header is used to calculate the number of
            # parameters needed [set as (?,....)].
            if key_auto:
                # If key is auto increment, then the code it is different:
                sql = f'''INSERT INTO {table_name}({','.join(table_header[1:])})
                     VALUES ({"?," * (number_fields - 1)}?)'''  # Number fields reduced for key.
            else:
                sql = f'''INSERT INTO {table_name}
                     VALUES ({"?," * number_fields}?)'''

            if method == 'multiple':
                # Multiple member selection.
                self.__cursor.executemany(sql, data)

            else:
                # Insert only one record (row) into database.
                self.__cursor.execute(sql, data)

            # Save the changes
            self.__db.commit()

        except sqlite3.IntegrityError as error:
            print(f'+-- ERROR: {error}.')
            print(f'+-- Process aborted.\n')
            # Rollback any changes if there is any issue.
            self.__db.rollback()

        except sqlite3.OperationalError as error:
            print(f'+-- ERROR: {error}.')
            print(f'+-- Process aborted.\n')
            # Rollback any changes if there is any issue.
            self.__db.rollback()

        else:
            # Only if all was ok.
            print('+-- New data inserted.\n')

    def update_database(self, sql_code: str) -> None:
        """
        UPDATE records in the db [not INSERT], this means that records will be committed to db.
        :param sql_code: SQL code to execute.
        :return: None.
        """
        try:
            # try-except to catch issues whilst updating the db.
            self.__cursor.execute(sql_code)
            # Save the changes
            self.__db.commit()

        except sqlite3.IntegrityError as error:
            print(f'+-- ERROR: {error}.')
            print(f'+- Process aborted.\n')
            # Rollback any changes.
            self.__db.rollback()

        except Exception as error:
            # Catch all. Used to update the code based on the possible error.
            print(f'+-- ERROR: {error}.')
            print(f'+- Process aborted.\n')
            # Rollback any changes.
            self.__db.rollback()

        else:
            # Only if all was ok.
            print('+- Data in database updated.\n')

    def gather_records(self, sql_code: str) -> list:
        """
        Execute some code to GATHER records from the db, then return the reply from database.
        :param sql_code: SQL code to execute.
        :return: Database reply --> Note this is a list!
        """
        self.__cursor.execute(sql_code)
        # Return the reply from database.
        return self.__cursor.fetchall()

    def show_all_data(self, table_name: str, header: list) -> None:
        """
        Print all data in db. SELECT * FROM table_name.
        :param table_name: Name of the table.
        :param header: Header of the table.
        :return: None.
        """
        # Select all records in the db.
        sql = f'''
                SELECT *
                FROM {table_name}
            '''
        # Using tabulate to pretty print.
        print(f'+----- Contents of table "{table_name}":-------+')
        print(tabulate(self.gather_records(sql), headers=header))
        print('+-----------------------------------------------+\n')

    def end_connection(self) -> None:
        """
        Close the connection to the database.
        :return: None.
        """
        print('+-- Closing database connection.')
        self.__db.close()


class UserTable(DataBase):
    """
    Class to handle and manage the UserTable in the program.
    """
    # User's data table:
    TABLE_USERS = 'userdata'
    TABLE_USERS_HEADER = ['username', 'password']
    # Fields for the user table.
    TABLE_USER_FIELDS = '''
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT
        '''

    def __init__(self):
        super().__init__()
        # Create UserTable
        self.create_table(self.TABLE_USERS, self.TABLE_USER_FIELDS)

    def add_data(self, new_user: str, new_password: str) -> bool:
        """
        Add new users/password to the db.
        Security for valid user/password must be defined outside.
        :param new_user: str. New user id.
        :param new_password: str. New password.
        :return: True if correct, False if none.
        """
        pre_users = len(self.gather_users_available())
        self.insert_records(
            data=(new_user, new_password),
            table_header=self.TABLE_USERS_HEADER,
            table_name=self.TABLE_USERS,
            method='single',
            key_auto=False
        )
        # Check if something new went in.
        if len(self.gather_users_available()) > pre_users:
            return True

        return False

    def retrieve_data(self,
                      select_command: str = '*',
                      where_command: str = '*',
                      type_filter: int = 0
                      ) -> list:
        """
        Manage gathering data from the database regarding SQL codes.
        Default behaviour is SELECT * FROM table_name;
        :param select_command: String to use in the SELECT SQL fragment.
        :param where_command: String to use in the WHERE SQL fragment.
        :param type_filter: Type of execution: 0 means without WHERE clause, 1 with WHERE.
        :return list: Return the values gathered in a list. If nothing was
            returned from DB, then empty list.
        """
        # Generate the SQL code to be used and do the search:
        sql = f'''
                SELECT {select_command}
                FROM {self.TABLE_USERS}'''
        if type_filter == 1:
            sql += f'''
                WHERE {where_command}'''

        # Send the search to the db and get the returned data (if any).
        search_result = self.gather_records(sql)
        if len(search_result) == 0:
            # No data
            return []

        else:
            return search_result

    def gather_users_available(self) -> list:
        """
        Gather all available users.
        :return: List with users.
        """
        # Gather all users.
        return self.from_db_item_to_list(self.retrieve_data(
                                              select_command=self.TABLE_USERS_HEADER[0],
                                              type_filter=0))

    def gather_password_for_user(self, username: str = None) -> list:
        """
        Retrieve the password stored for a particular user.
        :return: List with password (if found) or empty list (not found).
        """
        return self.retrieve_data(
            select_command=self.TABLE_USERS_HEADER[1],
            where_command=f'{self.TABLE_USERS_HEADER[0]} = "{username}"',
            type_filter=1
        )

    def check_login_details_correct(self, username: str, password: str) -> bool:
        """
        Check if the relation user-password it is correct.
        :param username: Username.
        :param password: Password.
        :return bool: True if it is correct, False otherwise.
        """
        password_stored = self.from_db_item_to_list(self.gather_password_for_user(username))
        if password_stored[0] == password:
            return True

        # Base case
        return False

    @staticmethod
    def from_db_item_to_list(to_convert: list):
        """
        Transform db data into a single list.
            From: [(item_i,), ...., (item_n,)]
            To: [item_i, ...., item_n]
        :param to_convert: list Format [(item_i,), ...., (item_n,)].
        :return: list format [item_i, ...., item_n]
        """
        return list(map(lambda x: ''.join(list(x[0])), to_convert))

    def __repr__(self):
        """Representation of the class."""
        return f'Class ({self.__class__.__name__}) that manage only the database table "{self.TABLE_USERS}".\n' \
               f'Header: {", ".join(self.TABLE_USERS_HEADER)}.'


if __name__ == '__main__':
    print('This is a class to manage a DataBase, please do not use as main.\n\n')
    user_db = UserTable()
    # Test create a new user:
    # user_db.add_data('test_user', 'test_pass_01')
    # Test see all db data:
    user_db.show_all_data(user_db.TABLE_USERS, user_db.TABLE_USERS_HEADER)
    # Test if gather data works.
    print('Correct!' if user_db.check_login_details_correct('test_user', 'test_pass_01') else 'Wrong..')
