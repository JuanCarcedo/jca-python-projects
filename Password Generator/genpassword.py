# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:17:24 2022
Generates random passwords:
    8/32 characteres long
    At least one letter
    At least one number
    At least one special character
@author: Juan CA
"""
from random import randint, shuffle, seed, sample
from datetime import datetime
import pandas as pd

# Constants
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
           'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
LEN_LETT = len(LETTERS)-1
LEN_SYMB = len(SYMBOLS)-1
LEN_NUMB = len(NUMBERS)-1


def create_password():
    """Create random password"""
    seed(datetime.now())
    password_letters = sample(LETTERS, randint(7, 10))
    password_symb = sample(NUMBERS, randint(2, 10))
    password_numb = sample(SYMBOLS, randint(2, 10))
    password = password_letters + password_symb + password_numb
    shuffle(password)
    if len(password) > 31:
        password = password[:32]
    password = ''.join(password)
    # Copy to the clipboard
    pd.DataFrame([password]).to_clipboard(index=False, header=False)
    return password
