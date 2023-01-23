"""
    main
    Program to test the class for DataFrame checks.
    :copyright: (c) 2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
from dataframecheck import DfInitCheck
import pandas as pd

if __name__ == '__main__':
    # --- Data exploration -- TESTs only ---
    file_to_check = 'example.csv'
    df_test = pd.read_csv(file_to_check)
    DfInitCheck.check_df(df_test)  # Check the dataframe
    # --- Data cleaning ---
    # Search for NaN data and delete if needed
    print('Checking dataframe for NaN values...')
    print(f'Deleted rows?: {DfInitCheck.remove_na(df_test)}')
