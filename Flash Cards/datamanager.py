# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 09:45:16 2022
Class DataManager to manage the data (jeje)
@author: jcara
"""

import pandas as pd
from random import randint


class DataManager(object):
    '''For now only spanish=english included.
    Modes: new_word, correct_answer, save_data'''

    def __init__(self, username):
        '''Init the class with the username'''
        # ---------------- Open user's files to_study and correct ---------- #
        self.username = username
        # Open to study file
        try:
            self.df = pd.read_csv(f'./data/{self.username}_es_en.csv',
                             encoding_errors='replace')
        except FileNotFoundError:
            # User has no file, therefore, gather default values
            self.df = pd.read_csv('./data/languages/original_es_en.csv',
                             encoding_errors='replace')
        # Open correct answers file
        try:
            self.df_correct = pd.read_csv(f'./data/{self.username}_es_en_correct.csv',
                                     encoding_errors='replace')
        except FileNotFoundError:
            # User has no file, therefore, initial DF (spanish english)
            self.df_correct = pd.DataFrame({'es': [], 'en': []})

    def new_word(self):
        ''' Select a new random word'''
        # ----------------- Select random word to study/check ------- #
        # Number of rows -- may change when correct answer
        df_rows = self.df[self.df.columns[0]].shape[0]
        # Get random item from data
        find = randint(0, df_rows)
        self.guess = self.df[self.df.columns[0]][find]
        self.solution = self.df[self.df.columns[1]][find]
        # Change type of retrieving index to prevent multiple choice
        # self.index = self.df.index[self.df[self.df.columns[0]] == self.guess].tolist()
        mask = (self.df[self.df.columns[0]] == self.guess) & (self.df[self.df.columns[1]] == self.solution)
        self.index = self.df[mask].index[0]

    def correct_answer(self):
        '''Move the correct answer to correct df and drop from base'''
        # --------------- Correct answer ----------------------- #
        try:
            # Correct answer moved to df correct
            self.df_correct = pd.concat([self.df_correct,
                                         self.df.iloc[[self.index]]],
                                        ignore_index=True)
        except AttributeError:
            pass
        else:
            # Correct value stored, therefore, drop from original file
            self.df = self.df.drop(self.index)  # [0])
            # in case of same word multiple answers, drop 1 of them

    def save_data(self):
        '''Store the current status'''
        # ----------------- User want to finish study lesson ---------------- #
        # Update the files --- Note index must be false
        # a. List of correct answers
        self.df_correct.to_csv(f'./data/{self.username}_es_en_correct.csv',
                               index=False)
        # b. List of actual answers
        self.df.to_csv(f'./data/{self.username}_es_en.csv', index=False)
