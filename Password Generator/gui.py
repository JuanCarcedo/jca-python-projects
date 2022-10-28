"""
    gui.py
    Control the GUI and processes
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
import tkinter as tk
import filemanagement as fm
import genpassword as gp

FONT = ('Consolas', 10, 'bold')
FONT_TITLE = ('Consolas', 25, 'bold')
JSON_FILE = 'data.json'


class InterfaceManager:

    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title('Password saver')
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
        lb_web = self.__gen_labels(name='Website')
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
        check = fm.add_to_file(mail=self.input_mail.get(),
                               password=self.input_pswrd.get(),
                               web=self.input_web.get())
        if check:
            self.clear_inputs()

    def search_data(self):
        fm.search_data_json(self.input_web.get())

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
        self.inpbox_pswrd.delete(0, tk.END)


if __name__ == '__main__':
    print('I am not supposed to be the main...')
