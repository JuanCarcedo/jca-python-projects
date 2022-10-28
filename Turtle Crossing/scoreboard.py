# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:18:17 2022
This program checks the levels
@author: Juan CA
@updates
    v2 20221028 - Save high score logic included - by JCA
"""
from turtle import Turtle

FONT = ("Courier", 25, "normal")
HIGH_SCORE = 'high_score_data.txt'  # V2 20221028 JCA


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.high_score = self.load_high_score()  # JCA 20221028 New
        self.level = 1
        self.goto(-280, 250)
        self.update_scoreboard()

    def level_up(self):
        self.level += 1
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Level: {self.level} High Score: {self.high_score}", align="left", font=FONT)  # V2 Updated

    def game_over(self):
        self.home()
        self.write("GAME OVER", align="center", font=FONT)
        # V2 20221028 JCA
        if self.level > self.high_score:
            self.high_score = self.level
            self.save_high_score()

    def load_high_score(self):  # V2 20221028 JCA
        try:
            with open(HIGH_SCORE) as file:
                return int(file.read())
        except FileNotFoundError:
            return 1

    def save_high_score(self):  # V2 20221028 JCA
        with open(HIGH_SCORE, mode='w') as file:
            file.write(str(self.high_score))
