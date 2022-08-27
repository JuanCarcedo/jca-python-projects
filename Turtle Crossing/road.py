# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 12:08:00 2022
Modify and display the road
@author: jcara
"""
from turtle import Turtle


class Road(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.roads = []
        self.create_limits()

    def create_limits(self):
        '''Create visual limits for the game'''
        # 260 / 240
        step = 60
        for i in range(-260, 240, step):
            self.goto(-300, i)
            self.pendown()
            self.goto(300, i)
            self.penup()
            self.roads.append(i + step/2)
