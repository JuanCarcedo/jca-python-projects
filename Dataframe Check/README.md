# DataFrame check
I developed this class to generate an overview of a new set of data.  
I was learning Data Science and Pandas. As I was nearly doing these checks every time I found a new set of data, I decided to create a class and re-use it.  
It is intended to give a detailed overview of a csv using Pandas.

## Instructions
- Create a Fork of the repository (you can access all projects).
- Open your favourite IDE (I use [PyCharm](https://www.jetbrains.com/pycharm/)).
- Check the ***[requirements.txt](https://github.com/JuanCarcedo/jca-python-projects/blob/main/requirements.txt)*** file.  
  - For this project you will need:
    + Pandas. 

Note: This is a no-GUI program, therefore you will see the outputs in the console.

## How to use
Note that you do not need to create an instance for the class, all methods are classmethods.
1) Copy into the folder a CSV file that you want to overview.
2) Change the _file_to_check_ variable in 'main.py' to the new file. Currently, it is:  
```file_to_check = 'example.csv'```
3) Run the file ```main.py```.
4) The program will print the overview.

Note that the DfInitCheck class can also remove na in the file using:  
```DfInitCheck.remove_na(df_test)```

## Example of output
Using the file ```example.csv``` provided, the output is:
```
---- Basic checks to overview the dataframe ----
Shape: 
- Rows: 637
- Columns: 3
Types of columns:
 DATE       object
CLOSE     float64
VOLUME    float64
dtype: object
Number of data per column:
DATE      637
CLOSE     636
VOLUME    636
dtype: int64

Basic data:               CLOSE        VOLUME
count    636.000000  6.360000e+02
mean    8153.865474  2.294152e+10
std     2413.429659  1.180037e+10
min     3399.471680  4.324201e+09
25%     6863.890625  1.528356e+10
50%     8707.169922  2.054569e+10
75%     9858.738281  2.990088e+10
max    13016.231445  7.415677e+10
Head:
         DATE        CLOSE        VOLUME
0  2019-01-01  3843.520020  4.324201e+09
1  2019-01-02  3943.409424  5.244857e+09
2  2019-01-03  3836.741211  4.530215e+09
3  2019-01-04  3857.717529  4.847965e+09
4  2019-01-05  3845.194580  5.137610e+09 
 Tail:
           DATE         CLOSE        VOLUME
632  2020-09-24  10745.548828  2.301754e+10
633  2020-09-25  10702.290039  2.123255e+10
634  2020-09-26  10754.437500  1.810501e+10
635  2020-09-27  10774.426758  1.801688e+10
636  2020-09-28  10912.536133  2.122653e+10
Found na values in columns:
DATE      0
CLOSE     1
VOLUME    1
dtype: int64
No duplicated values found.
---- ----------------------- ----
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 637 entries, 0 to 636
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   DATE    637 non-null    object 
 1   CLOSE   636 non-null    float64
 2   VOLUME  636 non-null    float64
dtypes: float64(2), object(1)
memory usage: 15.1+ KB
Checking dataframe for NaN values...
Deleted rows?: True
```

## Author and Licence
**[Juan Carcedo](https://github.com/JuanCarcedo)**  
2022 Copyright © - Licence [MIT](https://github.com/JuanCarcedo/jca-python-projects/blob/main/LICENSE.txt)
