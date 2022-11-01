# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:59:11 2022
Flashcard to learn Spanish
HOW TO IMPROVE THE CODE:
    Use df.to_dict(orient='records') to gather and use the data
        note rnd.choice()
    Use only 1 canvas (instead of front/back); just change the texts
    and the image whenever it flips.
        note: canvas.itemconfig(canvas_image, image=new_one)
@author: Juan CA
"""
from gui import InterfaceManager, GetUsername

if __name__ == '__main__':
    set_username = GetUsername()
    username = set_username.get_username()
    screen = InterfaceManager(username)
    screen.welcome_message()
    # END
    screen.end_screen()
