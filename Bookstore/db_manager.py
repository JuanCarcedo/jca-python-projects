"""
    Date: 23/12/2022
    db_manager
    Class to manage the database interaction.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
import sqlite3
from tabulate import tabulate  # Pretty tables


class DataBase:
    """
    Class to handle all items required with iterations with DB.
    """

    def __init__(self, path_to_db: str = 'abort'):
        """
        Constructor of the class. Note: path to db is required.
        :param path_to_db: File to be created.
        """
        assert path_to_db != 'abort', '+-- ERROR: Path to database is required for connection, process aborted.'
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
        print('+-- Creating new table.')
        try:
            # try-except block to prevent issues if the table is already there.
            sql_code = f'''
                CREATE TABLE {table_name} ({table_fields})'''
            # Get data into db and commit the change:
            self.__cursor.execute(sql_code)
            self.__db.commit()

        except sqlite3.OperationalError as error:
            # Catch the error if the table already exists.
            print(f'+-- ERROR: {error}.')
            print(f'+-- Process aborted.\n')

        except Exception as error:
            # Catch other errors.
            # Rollback any wrong changes.
            self.__db.rollback()
            raise error

        else:
            # Only if all goes well.
            print('+-- Table created.\n')

    def insert_records(self,
                       data,
                       table_header: list,
                       table_name: str,
                       method: str = 'multiple') -> None:
        """
        INSERT records in the database. Can insert one record or multiple ones using method.
        :param data: Data to insert into database (must be tuple for single insertion or
                    list of tuples for multiple insertion).
        :param table_header: Header of the table in List format.
        :param table_name: Name of table for inserting.
        :param method: 'single' for single insert, 'multiple' for multiple inserts.
        :return: None.
        """
        # Add data into the new table.
        print(f'+-- Adding {method} records into table "{table_name}".')

        try:
            # try-except to catch issues whilst updating the db.
            number_fields = len(table_header) - 1  # Reduced by 1 because one ? will be added manually.
            # Note: The length of the header is used to calculate the number of
            # parameters needed [set as (?,....)].
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


if __name__ == '__main__':
    print('This is a class to manage a DataBase, please do not use as main.')
