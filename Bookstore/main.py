"""
    Date: 23/12/2022
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
    Note:
        I created a Database with SQLiteStudio (3.4.1) stored in database/ebookstore.db
        A class will be managing interaction with database, all other menu options are
        handled by methods outside the class.
"""
# IMPORT ===============
import sqlite3
from tabulate import tabulate  # Pretty tables
from db_manager import DataBase  # DataBase management class

# CONSTANTS ===============
DATABASE_PATH = 'database/ebookstore.db'
MAIN_MENU = '''+-- Main menu:
+-\t1. Enter book
+-\t2. Update book
+-\t3. Delete book
+-\t4. Search books
+-\t5. Print full list of books
+-\t0. Exit'''

# Constants regarding the book table.
TABLE_BOOKS = 'books'
TABLE_BOOKS_HEADER = ['id', 'Title', 'Author', 'Qty']
# Fields for the table books.
TABLE_BOOKS_FIELDS = '''
    id INTEGER PRIMARY KEY,
    Title TEXT,
    Author TEXT,
    Qty INTEGER
    '''
# Note the list contains tuples: (id, title, author, quantity).
TABLE_BOOKS_INITIAL_VALUES = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
    (3006, 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 40),
    (3007, 'Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 40),
    (3008, 'The Two Towers', 'J.R.R Tolkien', 30),
    (3009, 'The Return of the King', 'J.R.R Tolkien', 30)
]


# METHODS =============================================================
def create_new_book(header: list, table_name: str) -> None:
    """
    Gather required inputs to create a new book.
    :param header: List with the headers of the table.
    :param table_name: Name of table to insert the records into.
    :return: None.
    """
    print('+-- Preparing to add a book. Please fill the following information.')
    # Selection of ID is left to the user; this can be automated with AUTO_INCREMENT.
    try:
        # try-except to prevent issues whilst doing a cast to int.
        new_id = int(input('+- Enter ID (it must be a number; example 3xxx): '))
        new_title = input('+- Enter title of book: ')
        new_author = input('+- Enter author of book: ')
        new_quantity = int(input('+- Enter quantity of books: '))

    except ValueError:
        print('+-- Only enter integers (numbers) when required.')
        print('+-- Process aborted.\n')

    else:
        # Insert new record in the db (single method).
        db.insert_records(data=(new_id, new_title, new_author, new_quantity),
                          table_header=header,
                          table_name=table_name,
                          method='single')


def search_for_book(header: list, table_name: str) -> None:
    """
    Search in the database all records with specific filters.
    :param header: List with the headers of the table.
    :param table_name: Name of table to insert the records into.
    :return: None.
    """
    print('+-- Search book(s).')
    search_filter = input(f'+- Please select which filter to use ({", ".join(header)}): ')
    # Check if the search_term is valid; if not print error message and return to menu.
    if search_filter not in header:
        print(f'+-- {search_filter} is not within the options.\n'
              '+-- Process aborted.\n')
        return

    search_value = input(f'+- Input {search_filter} to search for: ')
    try:
        # try-except block to prevent issues whilst doing cast into int.
        # If the value is an integer (id or quantity) it must be cast into int.
        # Else, it must be surrounded by "" as they are strings in database.
        if search_filter == 'id' or search_filter == 'Qty':
            search_value = int(search_value)
        else:
            search_value = f'\"{search_value}\"'

    except ValueError:
        print(f'+- ERROR: Please enter only a number when searching for {search_filter}.\n'
              f'+-- Process aborted.\n')
        return

    else:
        # Generate the SQL code to be used and do the search:
        sql = f'''
                SELECT *
                FROM {table_name}
                WHERE {search_filter} = {search_value}'''
        # Send the search to the db and get the returned data (if any).
        search_result = db.gather_records(sql)

        if len(search_result) == 0:
            # Empty list, therefore not found.
            print(f'+-- No record(s) with {search_filter} equal to {search_value}.\n')

        else:
            # Using tabulate to pretty print.
            print(f'+-- Record(s) with {search_filter} equal to {search_value}:')
            print(tabulate(search_result, headers=header))
            print('+-----------------------------------------------+\n')


def update_book_data(header: list, table_name: str) -> None:
    """
    Update the data of one book based on filters selected by user.
    :param header: List with the headers of the table.
    :param table_name: Name of table to insert the records into.
    :return: None.
    """
    print('+-- For security reasons updates can only be done selecting the ID of the record.')
    # Allow the user to do a search before updating the book (easier to gather IDs).
    if input('+- Would you like to search the book first (ID will be shown)? (y/n): ').lower() == 'y':
        search_for_book(header=header, table_name=table_name)

    try:
        # try-except block to prevent issues whilst doing cast into int for id and quantity (if selected)
        id_value = int(input('+- Please select ID of book to modify: '))
        # Generate the SQL code to search for the to-be modified book:
        sql = f'''
                        SELECT *
                        FROM {table_name}
                        WHERE {header[0]} = {id_value}'''
        # Send the search to the db and get the returned data (if any).
        search_result = db.gather_records(sql)

        if len(search_result) == 0:
            # Do not allow modification if the book does not exist.
            print(f'+-- The book selected could not be found.\n'
                  f'+-- Process aborted.\n')
            return

        print('+-- Please select the field to modify from the options below:')
        # Note that ID cannot be changed (security), therefore, ignored in the selection.
        field_to_modify = input(f'+- ({", ".join(header[1:])}) -> ')

        # Check if the field_to_modify is valid; if not print error message and return to menu.
        if (field_to_modify not in header) or field_to_modify.lower() == 'id':
            print(f'+-- ERROR: {field_to_modify} is not within the options.\n'
                  f'+-- Process aborted.\n')
            return

        # Gather the new value from user.
        new_value = input('+- Please input new value: ')
        # If the value is an integer (quantity) it must be cast into int.
        # Else, it must be surrounded by "" because the fields are strings in database.
        if new_value == 'Qty':
            new_value = int(new_value)
        else:
            new_value = f'\"{new_value}\"'

    except ValueError:
        print(f'+-- Please enter only a number when requested.\n'
              f'+-- Process aborted.\n')
        return

    else:
        # Generate the SQL code to be used; and send the update to the database.
        sql = f'''
                UPDATE {table_name}
                SET {field_to_modify} = {new_value}
                WHERE {header[0]} = {id_value}'''
        # Update db with new data.
        db.update_database(sql)
        print(f'+-- Changed {field_to_modify} to {new_value} for book {header[0]} equal {id_value}.\n')


def delete_book_data(header: list, table_name: str) -> None:
    """
    DELETE the data of one book based on the ID.
    :param header: List with the headers of the table.
    :param table_name: Name of table to insert the records into.
    :return: None.
    """
    print('+-- For security reasons, deletion can only be done selecting the ID of the record.')

    # Allow the user to do a search before deleting the book (easier to gather ID).
    if input('+- Would you like to search the book first (ID will be shown)? (y/n): ').lower() == 'y':
        search_for_book(header=header, table_name=table_name)

    try:
        # try-except block to prevent issues whilst doing cast into int for id.
        id_value = int(input('+- Please select ID of book to delete: '))

    except ValueError:
        print(f'+-- Please enter only a number when requested.\n'
              f'+-- Process aborted.\n')
        return

    else:
        # Generate the SQL code to search for the to-be deleted book:
        sql = f'''
                SELECT *
                FROM {table_name}
                WHERE {header[0]} = {id_value}'''
        # Send the search to the db and get the returned data (if any).
        search_result = db.gather_records(sql)

        # Do not allow deletion if the book does not exist.
        if len(search_result) == 0:
            print(f'+-- The book selected could not be found.\n'
                  f'+-- Process aborted.\n')
            return

        # Using tabulate to pretty print.
        print(f'+-- The following record will be deleted:')
        print(tabulate(search_result, headers=header))
        print('+-----------------------------------------------+\n')

        # Ask for a final confirmation
        if input('+- This cannot be undone. Continue? (y/n): ').lower() == 'y':
            # Generate the SQL code to be used; and send the deletion order to the database.
            sql = f'''
                    DELETE FROM {table_name}
                    WHERE {header[0]} = {id_value}'''
            db.update_database(sql)
            print(f'+-- Book {header[0]} equal {id_value} deleted.\n')

        else:
            print(f'+-- Process aborted.\n')


def initial_table_creation() -> None:
    """
    Create the table with initial data loaded.
    :return: None.
    """
    print(f'+-- Creating database table "{TABLE_BOOKS}" and inserting initial records.')

    # Create the table =================
    db.create_table(table_name=TABLE_BOOKS,
                    table_fields=TABLE_BOOKS_FIELDS)

    # Add data into the new table. =================
    print(f'+-- Adding initial records.')
    db.insert_records(data=TABLE_BOOKS_INITIAL_VALUES,
                      table_header=TABLE_BOOKS_HEADER,
                      table_name=TABLE_BOOKS,
                      method='multiple')


# MAIN =============================================================
if __name__ == '__main__':
    print(f'#{"-" * 10} Welcome to Bookstore Systems {"-" * 10}#')

    # Create the class to manage all database interactions.
    db = DataBase(DATABASE_PATH)

    # If it is the first time using the program, create the new table with some records.
    if input('+- Is this the first time running this program? (y/n) -> ').lower() == 'y':
        initial_table_creation()

    # Main loop for program.
    while True:
        # NOTE: In case there is an issue related to not having a table created,
        # the program will create it itself.
        try:
            # Catch ONLY issues if there is no database table created.
            print(MAIN_MENU)
            selection = input('+- Please select: ').lower()
            print('\n')

            if selection == '0':  # Close the db and exit the program.
                print(f'#-- Closing the system...\n')
                # IMPORTANT: Close the connection before leaving the program.
                db.end_connection()
                print(f'#{"-" * 10} Goodbye {"-" * 10}#')
                exit()

            elif selection == '1':  # Create/add a new book.
                create_new_book(header=TABLE_BOOKS_HEADER, table_name=TABLE_BOOKS)

            elif selection == '2':  # Update book's data.
                update_book_data(header=TABLE_BOOKS_HEADER, table_name=TABLE_BOOKS)

            elif selection == '3':  # Delete a book.
                delete_book_data(header=TABLE_BOOKS_HEADER, table_name=TABLE_BOOKS)

            elif selection == '4':  # Search book.
                search_for_book(header=TABLE_BOOKS_HEADER, table_name=TABLE_BOOKS)

            elif selection == '5':  # Print all data available.
                db.show_all_data(TABLE_BOOKS, TABLE_BOOKS_HEADER)

            else:
                print('+-- The selection is not valid.\n')

        except sqlite3.OperationalError as err:
            # Table not found, creating new table with records.
            print('+-- Something went wrong, reloading database table.\n')
            initial_table_creation()
