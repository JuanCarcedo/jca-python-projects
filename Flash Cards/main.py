# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:59:11 2022
Flashcard to learn Spanish (to English)
HOW TO IMPROVE THE CODE:
    Use df.to_dict(orient='records') to gather and use the data
        note rnd.choice()
    Use only 1 canvas (instead of front/back); just change the texts
    and the image whenever it flips.
        note: canvas.itemconfig(canvas_image, image=new_one)
@author: Juan CA
"""
# Imports
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datamanager import DataManager
# Comments
# flacar = flashcard; frt = front; bck = back

# Constants
FONT_CARD = ('Consolas', 30, 'bold')
FONT_TEXT = ('Consolas', 30, 'bold')
FONT_LANG = ('Consolas', 30, 'italic')
FLASHCARD_FRONT = "./images/flashcard_front_v2.png"
FLASHCARD_BACK = "./images/flashcard_back_v2.png"
BUTTON_W = "./images/icon_wrong_v2.png"
BUTTON_R = "./images/icon_right_v2.png"
BUTTON_REFRESH = "./images/icon_refresh_v2.png"
BUTTON_ANSW = "./images/icon_answer.png"
EXIT = "./images/exit.png"
BG_COLOR = '#A6F7C3'  # green
INIT_TEXT = '''Welcome to the self study method with flashcards.
This program will store your right answers and your wrong answers separately.
Note "nn" equals "ñ". Example castanna is castaña.
Exit button will exit the application and save data.
'''
ES = 'Spanish'
EN = 'English'


# Username
def get_username():
    # Get user's username:
    global window
    global input_username
    window = Tk()
    window.config(padx=10, pady=10)
    window.title('Log in')
    Label(window, text="Please, enter your username:",
              font=('Arial', 15)).pack()
    input_username = StringVar()
    entry_username = Entry(window, textvariable=input_username)
    entry_username.pack(padx=10, pady=10)
    entry_username.focus()
    Button(window, text='Ok', command=exit_user_window).pack()
    window.mainloop()


def exit_user_window():
    '''Close username window'''
    window.destroy()


def full_text_guess():
    '''Show full text if needed'''
    try:  # Check if error whilst getting data
        messagebox.showinfo(title='Full text', message=data.guess)
    except AttributeError:
        pass


def full_text_answer():
    '''Show full text if needed'''
    try:  # Check if error whilst getting data
        messagebox.showinfo(title='Full text', message=data.solution)
    except AttributeError:
        pass


def button_show_answer():
    '''Show the answer'''
    flashcard_front.grid_remove()  # Hide front
    flashcard_back.grid()  # Show back


# Buttons commands
def button_wrong():
    ''' Click when your guess was wrong'''
    button_refresh()  # For now same use


def button_right():
    ''' Click when your guess was right'''
    data.correct_answer()  # Move to right list and delete from current


def button_refresh():
    ''' Click refresh the word'''
    new_word()  # New word


def save_quit():
    '''Save data and quit application'''
    data.save_data()
    root.destroy()


# Load data
def new_word():
    '''Create a new word'''
    data.new_word()  # Create a new word
    # Hide answer
    flashcard_back.grid_remove()  # Hide back
    flashcard_front.grid()  # Show front again
    # Write the new word in the front flashcard
    flashcard_front.itemconfig(text_front_word, text=data.guess)
    flashcard_back.itemconfig(text_back_word, text=data.solution)


if __name__ == '__main__':
    # Build GUI ------------------------------------------------------------- #
    get_username()  # get the user's username
    # Main window
    root = Tk()
    root.title("Learn languages JC")
    root.configure(padx=20, pady=20, height=800, width=1400, bg=BG_COLOR)
    # Labels
    lb_title = Label(text=f'Hello, {input_username.get()}', font=FONT_TEXT,
                      justify='center', bg=BG_COLOR, fg='black')
    lb_title.grid(column=1, row=0, sticky='n')

    # Flashcard front -------------------------------------------------
    im_flacar_frt = PhotoImage(file=FLASHCARD_FRONT)
    flashcard_front = Canvas(root, width=600, height=300,
                            highlightthickness=0, bg=BG_COLOR)
    flashcard_front.create_image(300, 150, image=im_flacar_frt)
    text_word = 'Please click refresh button'
    text_front_word = flashcard_front.create_text(300, 180, text=text_word,
                                          font=FONT_CARD, fill='black')
    text_front_lang = flashcard_front.create_text(300, 90, text=ES,
                                          font=FONT_LANG, fill='black')
    # Canvas button full text
    bt_front_ft = Button(flashcard_front, text='Full text',
                         command=full_text_guess)
    bt_wind_front = flashcard_front.create_window(300, 255, window=bt_front_ft)
    # Display canvas
    flashcard_front.grid(column=0, row=1, columnspan=3, pady=(10, 10))
    # Flashcard back -- Initially hidden  -----------------
    imag_flacar_bck = PhotoImage(file=FLASHCARD_BACK)
    flashcard_back = Canvas(root, width=600, height=300,
                            highlightthickness=0, bg=BG_COLOR)
    flashcard_back.create_image(300, 150, image=imag_flacar_bck)
    text_answer = 'Hey! click refresh \nbutton first (no peeking!)'
    text_back_word = flashcard_back.create_text(300, 180, text=text_answer,
                                          font=FONT_CARD, fill='black')
    text_back_lang = flashcard_back.create_text(300, 90, text=EN,
                                          font=FONT_LANG, fill='black')
    # Canvas button full text
    bt_back_ft = Button(flashcard_back, text='Full text',
                         command=full_text_answer)
    bt_wind_back = flashcard_back.create_window(300, 255, window=bt_back_ft)
    flashcard_back.grid(column=0, row=1, columnspan=3, pady=(10, 10))
    flashcard_back.grid_remove()  # Hide the card to unhide call grid again
    # Buttons ------------------------------------ #
    # Wrong button
    img_w = Image.open(BUTTON_W)
    img_bt_wrong = ImageTk.PhotoImage(img_w)
    bt_wrong = Button(root, image=img_bt_wrong, command=button_wrong,
                      highlightthickness=0)
    bt_wrong.grid(column=0, row=2)  # , sticky='nw')
    # Right button
    img_r = Image.open(BUTTON_R).resize((100, 95))
    img_bt_right = ImageTk.PhotoImage(img_r)
    bt_right = Button(root, image=img_bt_right, command=button_right,
                      highlightthickness=0)
    bt_right.grid(column=2, row=2)  # , sticky='ne')
    # Refresh button
    img_ref = Image.open(BUTTON_REFRESH).resize((85, 88))
    img_bt_refresh = ImageTk.PhotoImage(img_ref)
    bt_refresh = Button(root, image=img_bt_refresh, command=button_refresh,
                        highlightthickness=0)
    bt_refresh.grid(column=0, row=0)  # , sticky='nw')
    # Exit button
    img_exit = Image.open(EXIT).resize((50, 50))
    img_bt_exit = ImageTk.PhotoImage(img_exit)
    bt_exit = Button(root, image=img_bt_exit, command=save_quit)
    bt_exit.grid(column=2, row=0)  # , sticky='ne')
    # button_show_answer
    img_ans = Image.open(BUTTON_ANSW)  # .resize((100, 68))
    img_bt_answer = ImageTk.PhotoImage(img_ans)
    bt_answer = Button(root, image=img_bt_answer, command=button_show_answer,
                      highlightthickness=0)
    bt_answer.grid(column=1, row=2)

    messagebox.showinfo(title='Welcome', message=INIT_TEXT)
    # Create the set of data
    data = DataManager(input_username.get())

    # END
    root.mainloop()
