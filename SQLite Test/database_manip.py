"""
    Date: 22/12/2022
    Description:
        Class to manage the database interactions in SQLite.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
# IMPORT ===============
import sqlite3
from tabulate import tabulate  # Pretty tables

# CONSTANTS ===============
DATABASE_PATH = 'data/student_db'

# Note the list contains tuples: (id, name, grade).
STUDENTS_HEADER = ['id', 'name', 'grade']
STUDENTS = [
    (55, 'Carl Davis', 61),
    (66, 'Dennis Fredrickson', 88),
    (77, 'Jane Richards', 78),
    (12, 'Peyton Sawyer', 45),
    (2, 'Lucas Brooke', 99),
]


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

    def show_all_data(self, table_name: str) -> None:
        """
        Print all data in db. SELECT * FROM table_name.
        :param table_name: Name of the table.
        :return: None.
        """
        # Select all records in the db.
        sql = f'''
                SELECT *
                FROM {table_name}
            '''
        # Using tabulate to pretty print.
        print(f'+----- Contents of table "{table_name}":-------+')
        print(tabulate(self.gather_records(sql), headers=STUDENTS_HEADER))
        print('+-----------------------------------------------+\n')

    def create_table(self, sql_code: str) -> None:
        """
        Create a new table. The code must be correct (no checks here).
        :param sql_code: Code to create a new table.
        :return: None.
        """
        # Generate the SQL code for the table:
        print('+-- Creating new table.')
        try:
            # try-except block to prevent issues if the table is already there.
            # Get data into db and commit the change:
            self.__cursor.execute(sql_code)
            self.__db.commit()

        except sqlite3.OperationalError as error:
            # Catch the error if the table already exists.
            print(f'+-- ERROR: {error}.')
            print(f'+- Process aborted.\n')

        except Exception as error:
            # Catch other errors.
            # Rollback any wrong changes.
            self.__db.rollback()
            raise error

        else:
            # Only if all goes well.
            print('+- Table created.\n')
        # I am not using finally because there are still things to do with the db.

    def insert_records(self, data, table_name: str, method: str = 'multiple') -> None:
        """
        Insert records in the database. Can insert one record or multiple ones using method.
        :param data: Data to insert into database (must be tuple for single insertion or
         list of tuples for multiple insertion).
        :param table_name: Name of table for inserting.
        :param method: 'single' for single insert, 'multiple' for multiple inserts.
        :return: None.
        """
        # Add data into the new table.
        print(f'+-- Adding {method} records into table "{table_name}".')

        try:
            # try-except to catch issues whilst updating the db.
            # Insert all records of data into the db.
            if method == 'multiple':
                # Multiple member selection. Note is "hardcoded" for this structure of table.
                # Probably in the future I will create something more dynamic.
                self.__cursor.executemany(f'''INSERT INTO {table_name} VALUES (?,?,?)''', data)

            else:
                # Prepared but not yet implemented.
                print('+- Single method not implemented.')
                return

            # Save the changes
            self.__db.commit()

        except sqlite3.IntegrityError as error:
            print(f'+-- ERROR: {error}.')
            print(f'+- Process aborted.\n')
            # Rollback any changes.
            self.__db.rollback()

        else:
            # Only if all was ok.
            print('+- New data inserted.\n')

    def gather_records(self, sql_code: str) -> list:
        """
        Execute some code to GATHER records from the db, then return the reply from database.
        :param sql_code: SQL code to execute.
        :return: Database reply --> Note this is a list!
        """
        self.__cursor.execute(sql_code)
        # Return the reply from database.
        return self.__cursor.fetchall()

    def update_database(self, sql_code: str) -> None:
        """
        UPDATE records in the db, this means that records will be committed to db.
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

    def end_connection(self) -> None:
        """
        Close the connection to the database.
        :return: None.
        """
        print('+- Closing database connection.')
        self.__db.close()


# MAIN =============================================================
if __name__ == '__main__':
    db_table = 'python_programming'  # DataBase table to be used.

    # Class to manage all db actions.
    db = DataBase(DATABASE_PATH)

    # Create the table =================
    # Generate the SQL code for the table:
    sql_command = f'''
        CREATE TABLE {db_table} (
            id INTEGER PRIMARY KEY,
            name TEXT,
            grade INTEGER
        )'''
    # Call the method to create the table:
    db.create_table(sql_command)

    # Add data into the new table. =================
    db.insert_records(STUDENTS, db_table, 'multiple')

    # Print status of db (not requested but nice to have) =================
    db.show_all_data(db_table)

    # Select all records with a grade between 60 and 80 =================
    # Generate the SQL code to be used.
    sql_command = f'''
        SELECT *
        FROM {db_table}
        WHERE grade BETWEEN 60 AND 80
    '''
    reply_from_db = db.gather_records(sql_command)

    # Using tabulate to pretty print.
    print('+-- Records with a grade between 60 and 80: =================+')
    print(tabulate(reply_from_db, headers=STUDENTS_HEADER))
    print('+-----------------------------------------------+\n')

    # Change Carl Davis’s grade to 65 =================
    print('+-- Changing Carl Davis\'s grade to 65. =================+')
    # Generate the SQL code to be used.
    sql_command = f'''
        UPDATE {db_table}
        SET grade = 65
        WHERE name = "Carl Davis"
    '''
    db.update_database(sql_command)

    # Print status of db after changing the db.
    db.show_all_data(db_table)

    # Delete Dennis Fredrickson’s row =================
    print('+-- Deleting Dennis Fredrickson. =================+')
    # Generate the SQL code to be used.
    sql_command = f'''
            DELETE FROM {db_table}
            WHERE name = "Dennis Fredrickson"
        '''
    db.update_database(sql_command)

    # Print status of db after changing the db.
    db.show_all_data(db_table)

    # Change the grade of all people with an id below 55 =================
    print('+-- Grade of all people with an id below 55 set to 33. =================+')
    # Generate the SQL code to be used.
    sql_command = f'''
                UPDATE {db_table}
                SET grade = 33
                WHERE id < 55
            '''
    # Note: Instructions say below 55, therefore, Carl Davis's grade (ID = 55) must not be changed.
    db.update_database(sql_command)

    # Print status of db after changing the db.
    db.show_all_data(db_table)

    # IMPORTANT: Close the connection before leaving the program.
    db.end_connection()
