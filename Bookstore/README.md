# BookStore
This program is meant to be a replica of a bookstore management system (no GUI).  
I am trying to show how to use a SQLite DB to store the bookstore data.  
Using my pre-coded class ```db_manager.py```, the interactions between database and main program should be easier.  
Note that tabulate is used to provide a clear and defined output.

## Instructions
- Create a Fork of the repository (you can access all projects).
- Open your favourite IDE (I use [PyCharm](https://www.jetbrains.com/pycharm/)).
- Check the ***[requirements.txt](https://github.com/JuanCarcedo/jca-python-projects/blob/main/requirements.txt)*** file.  
  - For this project you will need:
    + tabulate: To pretty print the outputs. 
    + [SQLite Studio](https://www.sqlitestudio.pl/) to check the DataBase content.

Note: This is a no-GUI program, therefore you will see the outputs in the console.

## How to use
Run the file ```main.py```.
Follow the instructions in the terminal (see Example of output for more details).
   - Explanations detailed in the next section with images.
   - Initial values are loaded into the db if it is the first time you execute the code.  

The main options are:
```
+-- Main menu:
+-	1. Enter book
+-	2. Update book
+-	3. Delete book
+-	4. Search books
+-	5. Print full list of books
+-	0. Exit
+- Please select: 
```
Input via terminal the action/option you wish to do.  
Note that the system will guide you through the options and fields that you need to input.

Feel free to try weird inputs; the program should handle exceptions well.

### Deleting a book:
Note that the system will require you to input the ID of the book in order to delete it.  
As this may be quite tricky, the system will ask if you wish to do a search first. After the search, the book(s) that fit the search will be delivered to the screen.  
See an example of a deletion below in (Example of output).

## Example of output
Welcome to system:  
```
#---------- Welcome to Bookstore Systems ----------#
+- Is this the first time running this program? (y/n) -> 
```
Select _y_ if it is the first time or _n_ if not.  
If the db table already exists, it will let you know:
```
+-- Creating database table "books" and inserting initial records.
+-- Creating new table.
+-- ERROR: table books already exists.
+-- Process aborted.

+-- Adding initial records.
+-- Adding multiple records into table "books".
+-- ERROR: UNIQUE constraint failed: books.id.
+-- Process aborted.
```

Main Menu:
```
+-- Main menu:
+-	1. Enter book
+-	2. Update book
+-	3. Delete book
+-	4. Search books
+-	5. Print full list of books
+-	0. Exit
+- Please select: 
```  

Full list of books option (using tabulate - option 5):  
```
+----- Contents of table "books":-------+
  id  Title                                     Author             Qty
----  ----------------------------------------  ---------------  -----
3001  A Tale of Two Cities                      Charles Dickens     30
3002  Harry Potter and the Philosopher's Stone  J.K. Rowling        40
3003  The Lion, the Witch and the Wardrobe      C. S. Lewis         25
3004  The Lord of the Rings                     J.R.R Tolkien       37
3005  Alice in Wonderland                       Lewis Carroll       12
3006  Harry Potter and the Chamber of Secrets   J.K. Rowling        40
3007  Harry Potter and the Prisoner of Azkaban  J.K. Rowling        40
3008  The Two Towers                            J.R.R Tolkien       30
3009  The Return of the King                    J.R.R Tolkien       30
+-----------------------------------------------+
```

Creating a new book (option 1):  
```
+-- Preparing to add a book. Please fill the following information.
+- Enter ID (it must be a number; example 3xxx): 3010
+- Enter title of book: Test Book
+- Enter author of book: Mr Tester
+- Enter quantity of books: 10
+-- Adding single records into table "books".
+-- New data inserted.
```

Delete book (option 3):
```
+-- For security reasons, deletion can only be done selecting the ID of the record.
+- Would you like to search the book first (ID will be shown)? (y/n): y
+-- Search book(s).
+- Please select which filter to use (id, Title, Author, Qty): Title
+- Input Title to search for: Test Book
+-- Record(s) with Title equal to "Test Book":
  id  Title      Author       Qty
----  ---------  ---------  -----
3010  Test Book  Mr Tester     10
+-----------------------------------------------+

+- Please select ID of book to delete: 3010
+-- The following record will be deleted:
  id  Title      Author       Qty
----  ---------  ---------  -----
3010  Test Book  Mr Tester     10
+-----------------------------------------------+

+- This cannot be undone. Continue? (y/n): y
+- Data in database updated.

+-- Book id equal 3010 deleted.
```

## Author and Licence
**[Juan Carcedo](https://github.com/JuanCarcedo)**  
2022 Copyright © - Licence [MIT](https://github.com/JuanCarcedo/jca-python-projects/blob/main/LICENSE.txt)
