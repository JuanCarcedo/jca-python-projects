"""
    gui.py
    Control the GUI and processes
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
import tkinter as tk
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
from filemanagement import JsonFileManager
import pandas as pd
import genpassword as gp

# CONSTANTS ========================
FONT = ('Consolas', 10, 'bold')
FONT_TITLE = ('Consolas', 25, 'bold')


class InterfaceManager(JsonFileManager):

    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title('Password Storage')
        self.__root.config(padx=20, pady=20, bg='gray')
        self.__basic_structure()
        self.__entry_fields()

    def end_screen(self):
        self.__root.mainloop()

    def __gen_labels(self, name: str = 'Empty'):
        """
        Generate a basic label.
        :param str name: Name for the label.
        :return: Label definition
        """
        assert name != 'Empty', 'Label definition is wrong in GUI class.'
        return tk.Label(text=name, font=FONT_TITLE,
                        justify='center', bg='gray', fg='white')

    def __basic_structure(self):
        lb_title = self.__gen_labels(name='Pass Storage')
        # Labels: Web, email and password
        lb_web = self.__gen_labels(name='From Where:')
        lb_mail = self.__gen_labels(name='Email/Username:')
        lb_pswrd = self.__gen_labels(name='Password:')
        # Display in screen
        lb_title.grid(column=1, row=0)
        lb_web.grid(column=0, row=1)
        lb_mail.grid(column=0, row=2)
        lb_pswrd.grid(column=0, row=3)

    def __entry_fields(self):
        # Entry types: Web, email and password
        self.input_web = tk.StringVar()
        self.inpbox_web = tk.Entry(width=32, textvariable=self.input_web)
        self.inpbox_web.grid(column=1, row=1, sticky='w')  # v3 updated
        self.inpbox_web.focus()
        self.input_mail = tk.StringVar()
        self.inpbox_mail = tk.Entry(textvariable=self.input_mail)
        self.inpbox_mail.insert(tk.END, 'used_email@gmail.com')
        self.inpbox_mail.grid(column=1, row=2, columnspan=2, sticky=tk.W + tk.E)
        self.input_pswrd = tk.StringVar()
        self.inpbox_pswrd = tk.Entry(width=32, textvariable=self.input_pswrd)
        self.inpbox_pswrd.grid(column=1, row=3, sticky='w')
        # Buttons
        bt_password = tk.Button(text='Generate Password', command=self.new_password)
        # bt_password.config(padx=2, pady=2)
        bt_password.grid(column=2, row=3, padx=3, pady=3)
        # Add to txt row
        bt_file = tk.Button(text='Add', command=self.update_file)
        bt_file.config(padx=2, pady=2)
        bt_file.grid(column=1, row=4, columnspan=2, sticky=tk.W + tk.E)
        # Search --- added in v3
        bt_search = tk.Button(width=13, text='Search', command=self.search_data)
        bt_search.grid(column=2, row=1, padx=3, pady=3)

    # ---------------- Methods from buttons ------------- #
    def update_file(self):
        """ Refresh the file's data.
            Checks parameters before adding data.
        """
        input_fields = (self.input_web.get(), self.input_mail.get(), self.input_pswrd.get())
        if not input_fields[0] or not input_fields[1] or not input_fields[2]:
            InterfaceManager.pop_up(title='Warning', message='Empty fields.', type_mess='warning')

        else:  # All fields filled
            message = f'Email: {self.input_mail.get()}\n Password: {self.input_pswrd.get()}\n is this ok?'
            if InterfaceManager.pop_up(title='Review fields', message=message, type_mess='yesno'):
                if self.create_file_json(mail=input_fields[1], password=input_fields[2], web=input_fields[0]):
                    self.clear_inputs()

    def search_data(self):
        """Search in the data for the website/place. Retrieve the values in a popup."""
        web_search = self.input_web.get()
        if web_search:  # not empty
            title, message, message_type, password = self.search_data_json(web_search)
            # Copy password to clipboard
            self.copy_to_clipboard(password)

        else:
            title, message, message_type = 'Warning', 'From Where is empty', 'warning'

        InterfaceManager.pop_up(title=title, message=message, type_mess=message_type)

    def new_password(self):
        """
        Generate a new password every time is called
        """
        # Update password field
        self.inpbox_pswrd.delete(0, tk.END)
        self.inpbox_pswrd.insert(0, gp.create_password())

    # -------- Other methods ------ #
    def clear_inputs(self):
        """
        Cleans all parameters from screen (new input)
        """
        self.inpbox_web.delete(0, tk.END)
        self.inpbox_mail.delete(0, tk.END)
        self.inpbox_pswrd.delete(0, tk.END)

    def copy_to_clipboard(self, item):
        """Copy an item to the clipboard."""
        pd.DataFrame([item.strip()]).to_clipboard(index=False, header=False)

    # 2023-JCA-New classmethod
    @classmethod
    def pop_up(cls, title: str = '', message: str = '', type_mess: str = ''):
        """
        Generate messages when requested.
        :param str title: Title of the message.
        :param str message: Message to display.
        :param str type_mess: Selection of kind of message; warning, error, info or yesno.
        :return: Only with yesno, other -> None
        """
        if type_mess == 'warning':
            showwarning(title=title, message=message)
        elif type_mess == 'error':
            showerror(title=title, message=message)
        elif type_mess == 'info':
            showinfo(title=title, message=message)
        elif type_mess == 'yesno':
            return askyesno(title=title, message=message)
        else:
            pass
        return None


if __name__ == '__main__':
    print('I am not supposed to be the main...')
