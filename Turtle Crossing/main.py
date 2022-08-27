# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:13:12 2022
Main program for turtle crossing game
@author: jcara
"""
from scoreboard import Scoreboard
from player import Player
from car import Car
from road import Road
import turtle as tr
import importlib
import time


# Constants

# To work in Spyder
importlib.reload(tr)
# Create screen
screen = tr.Screen()
screen.setup(width=600, height=600)
screen.title("Turtle crossing the road")
screen.tracer(0)
# Create the road
road = Road()
# Create Turtle
turtle = Player()
# Create other items
scoreboard = Scoreboard()
cars = Car(road.roads[:-1])
# Create a bunch of cars


# Game starts
screen.listen()
screen.onkey(turtle.go_up, "Up")

game_is_on = True
while game_is_on:
    screen.update()  # refresh screen
    time.sleep(cars.move_speed)
    tur_y_cor = turtle.ycor()
    # Create random new cars (LIMIT == 10)
    cars.update_cars()  # Create new car
    # Move cars
    cars.move()
    # Detect collision
    for vehicle in cars.car_list:
        if turtle.distance(vehicle.xcor(), vehicle.ycor()) < 22:
            screen.update()
            game_is_on = False
            scoreboard.game_over()
    # Check if turtle won (playground -260, 260)
    if tur_y_cor >= 260:  # Turtle won
        turtle.restart_turtle()
        scoreboard.level_up()
        cars.move_speed *= 0.9  # Update speed
# END
screen.exitonclick()
