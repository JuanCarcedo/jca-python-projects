# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:13:12 2022
Main program for turtle crossing game.
Use the up key to move the turtle, no other movement is allowed.
@author: Juan CA
"""
from scoreboard import Scoreboard
from player import Player
from car import Car
from road import Road
import turtle as tr
import time

WIDTH = 600
HEIGHT = 600
SPEED_INCREASE = 0.9


if __name__ == '__main__':
    # Create screen
    screen = tr.Screen()
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.title("Turtle crossing the road")
    screen.tracer(0)
    # Creation of items
    road = Road()
    turtle = Player()
    scoreboard = Scoreboard()
    cars = Car(road.roads[:-1])
    # Start Game
    screen.listen()
    screen.onkey(turtle.go_up, "Up")
    game_is_on = True
    while game_is_on:
        screen.update()
        time.sleep(cars.move_speed)
        tur_y_cor = turtle.ycor()
        cars.update_cars()  # Create new car
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
            cars.move_speed *= SPEED_INCREASE  # Update speed
    # END
    screen.exitonclick()
