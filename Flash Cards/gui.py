"""
    gui.py
    Control the gui and other methods.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datamanager import DataManager

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


class GetUsername:
    """
    Manage the username's first inputs
    """
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.config(padx=10, pady=10)
        self.__window.title('Log in')
        self.__basic_structure()
        self.__window.mainloop()

    def __basic_structure(self):
        tk.Label(self.__window, text="Please, enter your username:",
                 font=('Arial', 15)).pack()
        self.input_username = tk.StringVar()
        entry_username = tk.Entry(self.__window, textvariable=self.input_username)
        entry_username.pack(padx=10, pady=10)
        entry_username.focus()
        tk.Button(self.__window, text='Ok', command=lambda: self.__window.destroy()).pack()

    def get_username(self):
        return self.input_username.get()


class InterfaceManager:

    def __init__(self, username: str = None):
        assert username, 'Please check username input. Something went wrong.'
        self.username = username
        self.data = DataManager(username)
        self.__root = tk.Tk()
        self.__root.title('Learn languages JCA')
        self.__root.configure(padx=20, pady=20, height=800, width=1400, bg=BG_COLOR)
        self.__create_structure()

    def welcome_message(self):
        messagebox.showinfo(title='Welcome', message=INIT_TEXT)

    def end_screen(self):
        self.__root.mainloop()

    def __create_structure(self):
        lb_title = tk.Label(text=f'Hello, {self.username}', font=FONT_TEXT,
                            justify='center', bg=BG_COLOR, fg='black')
        lb_title.grid(column=1, row=0, sticky='n')
        self.__flash_cards()
        self.__buttons()

    def __flash_cards(self):
        # Flashcard front -------------------------------------------------
        self.im_flacar_frt = tk.PhotoImage(file=FLASHCARD_FRONT)
        self.fc_front = tk.Canvas(self.__root,
                                  width=600, height=300,
                                  highlightthickness=0, bg=BG_COLOR)
        self.fc_front.create_image(300, 150, image=self.im_flacar_frt)
        text_word = 'Please click refresh button'
        self.txt_front = self.fc_front.create_text(300, 180,
                                                   text=text_word,
                                                   font=FONT_CARD,
                                                   fill='black')
        text_front_lang = self.fc_front.create_text(300, 90,
                                                    text=ES,
                                                    font=FONT_LANG,
                                                    fill='black')
        # Canvas button full text
        self.bt_front_ft = tk.Button(self.fc_front,
                                text='Full text',
                                command=lambda: self.show_full_text(self.data.guess))
        bt_wind_front = self.fc_front.create_window(300, 255, window=self.bt_front_ft)
        # Display canvas
        self.fc_front.grid(column=0, row=1, columnspan=3, pady=(10, 10))
        # Flashcard back -- Initially hidden  -----------------
        self.imag_flacar_bck = tk.PhotoImage(file=FLASHCARD_BACK)
        self.fc_back = tk.Canvas(self.__root, width=600, height=300,
                                 highlightthickness=0, bg=BG_COLOR)
        self.fc_back.create_image(300, 150, image=self.imag_flacar_bck)
        text_answer = 'Hey! click refresh \nbutton first (no peeking!)'
        self.txt_back = self.fc_back.create_text(300, 180,
                                                 text=text_answer,
                                                 font=FONT_CARD,
                                                 fill='black')
        text_back_lang = self.fc_back.create_text(300, 90,
                                                  text=EN,
                                                  font=FONT_LANG,
                                                  fill='black')
        # Canvas button full text
        self.bt_back_ft = tk.Button(self.fc_back,
                               text='Full text',
                               command=lambda: self.show_full_text(self.data.solution))
        bt_wind_back = self.fc_back.create_window(300, 255, window=self.bt_back_ft)
        self.fc_back.grid(column=0, row=1, columnspan=3, pady=(10, 10))
        self.fc_back.grid_remove()  # Hide the card to unhide call grid again

    def __buttons(self):
        # Load images for buttons // Create the button // Put in grid
        self.img_w = Image.open(BUTTON_W)
        self.img_bt_wrong = ImageTk.PhotoImage(self.img_w)
        self.bt_wrong = tk.Button(self.__root, image=self.img_bt_wrong,
                             command=self.bt_wrong, highlightthickness=0)
        self.bt_wrong.grid(column=0, row=2)  # , sticky='nw')
        self.img_r = Image.open(BUTTON_R).resize((100, 95))
        self.img_bt_right = ImageTk.PhotoImage(self.img_r)
        self.bt_right = tk.Button(self.__root, image=self.img_bt_right,
                             command=self.bt_correct, highlightthickness=0)
        self.bt_right.grid(column=2, row=2)  # , sticky='ne')
        self.img_ref = Image.open(BUTTON_REFRESH).resize((85, 88))
        self.img_bt_refresh = ImageTk.PhotoImage(self.img_ref)
        self.bt_refresh = tk.Button(self.__root, image=self.img_bt_refresh,
                               command=self.get_new_word, highlightthickness=0)
        self.bt_refresh.grid(column=0, row=0)  # , sticky='nw')
        self.img_exit = Image.open(EXIT).resize((50, 50))
        self.img_bt_exit = ImageTk.PhotoImage(self.img_exit)
        self.bt_exit = tk.Button(self.__root, image=self.img_bt_exit,
                            command=self.save_quit)
        self.bt_exit.grid(column=2, row=0)  # , sticky='ne')
        self.img_ans = Image.open(BUTTON_ANSW)
        self.img_bt_answer = ImageTk.PhotoImage(self.img_ans)
        self.bt_answer = tk.Button(self.__root, image=self.img_bt_answer,
                              command=self.bt_show_answer, highlightthickness=0)
        self.bt_answer.grid(column=1, row=2)

    # ---- Buttons behaviour ----- #
    def save_quit(self):
        self.data.save_data(self.username)
        self.__root.destroy()

    def get_new_word(self):
        self.data.new_word()
        # Hide the answer
        self.fc_back.grid_remove()
        self.fc_front.grid()
        # Write new word in the front flashcard
        self.fc_front.itemconfig(self.txt_front, text=self.data.guess)
        self.fc_back.itemconfig(self.txt_back, text=self.data.solution)

    def bt_correct(self):
        self.data.correct_answer()

    def bt_wrong(self):
        self.get_new_word()

    def bt_show_answer(self):
        self.fc_front.grid_remove()
        self.fc_back.grid()

    def show_full_text(self, message):
        try:  # Check if error whilst getting data
            messagebox.showinfo(title='Full text', message=message)
        except AttributeError:
            pass


if __name__ == '__main__':
    print('I am not meant to be executed as a main...')
