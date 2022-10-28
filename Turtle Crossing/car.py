# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:51:06 2022
This class controls and creates new cars
@author: Juan CA
"""
from turtle import Turtle
import random as rnd
from datetime import datetime

MOVE_DISTANCE = 20


class Car:

    def __init__(self, roads):
        self.car_list = []
        self.y_positions = roads
        self.add_car()
        self.move_speed = 0.1

    def add_car(self):
        """New car to the list"""
        new_car = Turtle(shape="square")
        new_car.penup()
        new_car.color(self.rand_color())  # Random
        new_car.shapesize(stretch_len=2, stretch_wid=1)
        rnd.seed(datetime.now())
        y_pos = rnd.choice(self.y_positions)
        new_car.goto(320, y_pos)
        self.car_list.append(new_car)

    def move(self):
        for car in self.car_list:
            new_x = car.xcor() - MOVE_DISTANCE
            car.goto(new_x, car.ycor())
            self.end_road(car)

    def reset_position(self, car):
        rnd.seed(datetime.now())
        y_pos = rnd.choice(self.y_positions)
        car.goto(320, y_pos)

    def end_road(self, car):
        """Check if it is the end of the road"""
        if car.xcor() < -300:  # End reached
            self.reset_position(car)

    def rand_color(self):
        """Returns random color in hexadecimal"""
        return "#"+''.join([rnd.choice('ABCDEF0123456789') for i in range(6)])

    def update_cars(self):
        rnd.seed(datetime.now())
        if rnd.randint(1, 10) > 7 and len(self.car_list) < 11:
            self.add_car()
