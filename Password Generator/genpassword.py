# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:17:24 2022
Class that generates random passwords:
## Password:
    8/32 characteres long
    At least one letter
    At least one number
    At least one special character
@author: jcara
"""
from random import choice, randint, shuffle, seed
from datetime import datetime

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


class GenPassword:
    '''Generates random passwords'''

    def __init__(self):
        self.password = []
        self.create_password()
        shuffle(self.password)

    def create_password(self):
        '''Create random password'''
        seed(datetime.now())
        num_let = randint(7, 10)
        num_sym = randint(2, 10)
        num_num = randint(2, 10)
        # V1 -- Works as V0 although less lines
        password_letters = [choice(LETTERS) for _ in range(num_let)]
        password_symb = [choice(NUMBERS) for _ in range(num_sym)]
        password_numb = [choice(SYMBOLS) for _ in range(num_num)]
        self.password = password_letters + password_symb + password_numb
        # # V0 # Add random items to the password
        # while num_let != 0:
        #     self.password.append(LETTERS[randint(0, LEN_LETT)])
        #     num_let -= 1  # reduce value of letters left
        # # Adding Numbers
        # while num_num != 0:
        #     self.password.append(NUMBERS[randint(0, LEN_NUMB)])
        #     num_num -= 1  # reduce value of letters left
        # # Adding Symbols
        # while num_sym != 0:
        #     self.password.append(SYMBOLS[randint(0, LEN_SYMB)])
        #     num_sym -= 1  # reduce value of letters left
        # while len(self.password) < 8:
        #     self.password.append(LETTERS[randint(0, LEN_LETT)])
        #     self.password.append(NUMBERS[randint(0, LEN_NUMB)])
        #     self.password.append(SYMBOLS[randint(0, LEN_SYMB)])
