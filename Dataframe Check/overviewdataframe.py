"""
    overviewdataframe
    Return in terminal a list of handy checks for Pandas df.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""

import pandas as pd


class DfInitCheck:
    """
        Use check_df class method to run some basic checks.
        Delete na members with remove_na
    """
    @classmethod
    def check_df(cls, df_check) -> None:
        """Useful checks to see df data """
        print('\n\n---- Basic checks to overview the dataframe ----')
        print(f'Shape: \n- Rows: {df_check.shape[0]}\n- Columns: {df_check.shape[1]}')
        print(f'Types of columns:\n {df_check.dtypes}')
        # print(f'Column names: {df_check.columns}')
        print(f'Number of data per column:\n{df_check.count()}\n')
        pd.options.display.max_columns = None  # Prompt to show all columns
        print(f'Basic data: {df_check.describe()}')
        print(f'Head:\n{df_check.head()} \n Tail:\n{df_check.tail()}')
        # na values
        if df_check.isna().values.any():
            print('Found na values in columns:')
            print(df_check.isna().sum())
        else:
            print('No na values.')
        # duplicated values
        if df_check.duplicated().values.any():
            print(f'There are {len(df_check[df_check.duplicated()])} duplicated values.')
        else:
            print('No duplicated values found.')
        print('---- ----------------------- ----')
        df_check.info()

    @classmethod
    def remove_na(cls, df_check) -> bool:
        if df_check.isna().values.any():
            # print(df_check[df_check.isna().values == True])  # Show the NaN values
            df_check.dropna(inplace=True)  # Drop the NaN values
            return True
        return False

    def __str__(self):
        return 'Please use a DataFrame as argument. Expected return is a set of commands in terminal.'


if __name__ == '__main__':
    # --- Data exploration -- TESTs only ---
    df_test = pd.read_csv('Daily BTC price.csv')
    DfInitCheck.check_df(df_test)  # Check the dataframe
    # --- Data cleaning ---
    # Search for NaN data and delete if needed
    print('Checking dataframe for NaN values...')
    print(f'Deleted rows?: {DfInitCheck.remove_na(df_test)}')
