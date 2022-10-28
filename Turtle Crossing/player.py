# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:27:48 2022
This class keeps track of the turtle for the player
@author: Juan CA
"""
from turtle import Turtle

MOVE_DISTANCE = 30
INITIAL_PLACE = (0, -280)


class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.restart_turtle()

    def go_up(self):
        new_y = self.ycor() + MOVE_DISTANCE
        self.goto(0, new_y)

    def restart_turtle(self):
        self.goto(INITIAL_PLACE)
        self.setheading(90)
