# Database Tests
This program was created to test class DataBase.  
This class will be reused (and sometimes enhanced) in multiple of my projects as a standard when dealing with a database.
### Note:
- Tabulate is used for pretty print the outputs.  
- Inside "data/" folder the original database is kept.  
- Check "result/" to see the outcome of the program.

## Instructions
***

- Create a Fork of the repository (you can access all projects).
- Open your favourite IDE (I use [PyCharm](https://www.jetbrains.com/pycharm/)).
- Check the ***[requirements.txt](https://github.com/JuanCarcedo/jca-python-projects/blob/main/requirements.txt)*** file.  
  - For this project you will need:
    + tabulate.
    + [SQLite Studio](https://www.sqlitestudio.pl/) to check the DataBase content.

Note:  
- This is a no-GUI program, therefore you will see the outputs in the console.  
- The file inside **data** folder is a blank database. It will be filled once the code runs.

## How to use
***
1) Run the file ```main.py```.
2) Open SQLite Studio and connect to the database inside **result** folder.  

You can see/check that the expected modifications are done (check the Example of output).

## Example of output
***
Original data:  
```python
STUDENTS = [
    (55, 'Carl Davis', 61),
    (66, 'Dennis Fredrickson', 88),
    (77, 'Jane Richards', 78),
    (12, 'Peyton Sawyer', 45),
    (2, 'Lucas Brooke', 99),
]
```

Output in console:  
```
+-- Creating new table.
+- Table created.

+-- Adding multiple records into table "python_programming".
+- New data inserted.

+----- Contents of table "python_programming":-------+
  id  name                  grade
----  ------------------  -------
   2  Lucas Brooke             99
  12  Peyton Sawyer            45
  55  Carl Davis               61
  66  Dennis Fredrickson       88
  77  Jane Richards            78
+-----------------------------------------------+

+-- Records with a grade between 60 and 80: =================+
  id  name             grade
----  -------------  -------
  55  Carl Davis          61
  77  Jane Richards       78
+-----------------------------------------------+

+-- Changing Carl Davis's grade to 65. =================+
+- Data in database updated.

+----- Contents of table "python_programming":-------+
  id  name                  grade
----  ------------------  -------
   2  Lucas Brooke             99
  12  Peyton Sawyer            45
  55  Carl Davis               65
  66  Dennis Fredrickson       88
  77  Jane Richards            78
+-----------------------------------------------+

+-- Deleting Dennis Fredrickson. =================+
+- Data in database updated.

+----- Contents of table "python_programming":-------+
  id  name             grade
----  -------------  -------
   2  Lucas Brooke        99
  12  Peyton Sawyer       45
  55  Carl Davis          65
  77  Jane Richards       78
+-----------------------------------------------+

+-- Grade of all people with an id below 55 set to 33. =================+
+- Data in database updated.

+----- Contents of table "python_programming":-------+
  id  name             grade
----  -------------  -------
   2  Lucas Brooke        33
  12  Peyton Sawyer       33
  55  Carl Davis          65
  77  Jane Richards       78
+-----------------------------------------------+

+- Closing database connection.

Process finished with exit code 0

```

Output table:     
![db_output](/readme_images/db_result.PNG)

## Author and Licence
****
**[Juan Carcedo](https://github.com/JuanCarcedo)**  
2022 Copyright © - Licence [MIT](https://github.com/JuanCarcedo/jca-python-projects/blob/main/LICENSE.txt)