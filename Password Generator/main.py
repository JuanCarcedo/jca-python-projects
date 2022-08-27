# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 13:46:58 2022
Password generator and storage v3
@author: jcara
New in v3:
    Search capability --> with txt is df json is with read
    New error messages
    txt file changed to json
"""
import tkinter as tk
import genpassword as gp  # Password generator
import pandas as pd  # Copy to clipboard
import json  # json module to build json files

# Constants or other definitions
FONT = ('Consolas', 10, 'bold')
FONT_TITLE = ('Consolas', 25, 'bold')
DATA_FILE = 'data.txt'
JSON_FILE = 'data.json'
# Definitions


def new_password():
    '''Creates a new password every time is called'''
    global password
    password = gp.GenPassword().password
    if len(password) > 31:
        password = password[:32]
    password = ''.join(password)
    # Copy to the clipboard
    pd.DataFrame([password]).to_clipboard(index=False, header=False)
    # Put the text in the password field
    inpbox_pswrd.delete(0, tk.END)
    inpbox_pswrd.insert(0, password)


def warning_pop_up():
    '''Controls pop ups'''
    tk.messagebox.showwarning(title='Warning',
                              message="Empty fields")


# ------------- Not used in v3.ii ------------------------------------ #
def create_file_txt():
    '''Generate a txt file'''
    # Open file if it exists
    with open(DATA_FILE, mode='a') as file:  # a points to the end of file
        file.write(f'{input_web.get()}\t{input_mail.get()}\t{input_pswrd.get()}\n')
# -------------------------------------------------- #


def create_file_json():
    '''Generate a json file'''
    new_data = {
        input_web.get(): {
            "username": input_mail.get(),
            "pass": input_pswrd.get()
        }
    }
    try:  # Error if file does not exist
        with open(JSON_FILE, mode='r') as file:
            data_json = json.load(file)  # Get available data
    except FileNotFoundError:
        with open(JSON_FILE, mode='w') as file:
            json.dump(new_data, file, indent=2)  # dump into file
    else:
        data_json.update(new_data)  # Append new values
        with open(JSON_FILE, mode='w') as file:
            json.dump(data_json, file, indent=2)  # dump into file


def clean_screen():
    '''Cleans all parameters from screen (new input)'''
    inpbox_web.delete(0, tk.END)
    inpbox_pswrd.delete(0, tk.END)


def add_to_file():
    '''Control adding to file'''
    if not input_mail.get() or not input_pswrd.get() or not input_web.get():
        # if any is empty then here
        warning_pop_up()
    else:  # All fields filled
        # Review data
        review_ok = tk.messagebox.askyesno(title='Review fields',
                               message=f'Email: {input_mail.get()}\n Password: {input_pswrd.get()}\n is this ok?')    
        if review_ok:
            create_file_json()  # json file
            # create_file_txt()  # txt file
            # Clean file after write
            clean_screen()


# ------------- Not used in v3.ii ------------------------------------ #
def search_data_txt():  # Added in v3
    '''Search the Website and username in the db
        returns the username and password if found (txt)'''
    # Below to search based on txt file and df
    # file_user -- create the df
    df = pd.read_csv(DATA_FILE, sep='\t', header=None)
    df.rename(columns={0: 'web', 1: 'username', 2: 'pass'}, inplace=True)
    # Get only the data that we are looking for
    search = df.loc[df['web'] == input_web.get()]
    if search.empty:  # True if it is empty
        tk.messagebox.showinfo(title='Search result', message="Domain not found")
    else:  # data found
        search = search.values.tolist()
        tk.messagebox.showinfo(title=search[0][0], message=f'Email/Username: {search[0][1]}\n Password: {search[0][2]}')
# -------------------------------------------------- #


def search_data_json():  # Search capability with json files
    '''Search the Website and username in the db
        returns the username and password if found (json)'''
    web_search = input_web.get()
    if web_search:  # not empty
        try:
            with open(JSON_FILE) as file:
                json_data = json.load(file)
        except FileNotFoundError:
            tk.messagebox.showerror(title="Error", message="No file with data found.")
        else:
            # Can be done with try with keyerror but, note that errors is something
            # to catch an error that will not normally happen or it is complex to
            # handle elsewhere or with if/else
            if web_search in json_data:  # Key in there
                user = json_data[web_search]['username']
                password = json_data[web_search]['pass']
                text = f"Username: {user}\nPassword: {password}"
            else:
                text = f"No data for {web_search}"
            tk.messagebox.showinfo(title='Search result', message=text)
    else:
         tk.messagebox.showwarning(title="Warning", message="Website is empty.")


# Main code
# root creation
root = tk.Tk()
root.title('Password saver')
root.config(padx=20, pady=20, bg='gray')


# Title
lb_title = tk.Label(text='Pass Storage', font=FONT_TITLE
                    , justify='center', bg='gray', fg='white')
lb_title.grid(column=1, row=0)
# Labels: Web, email and password
lb_web = tk.Label(text='Website:', font=FONT,
                  justify='center', bg='gray', fg='white')
lb_web.grid(column=0, row=1)
lb_mail = tk.Label(text='Email/Username:', font=FONT,
                   justify='center', bg='gray', fg='white')
lb_mail.grid(column=0, row=2)
lb_pswrd = tk.Label(text='Password:', font=FONT,
                    justify='center', bg='gray', fg='white')
lb_pswrd.grid(column=0, row=3)

# Entry types: Web, email and password
input_web = tk.StringVar()
inpbox_web = tk.Entry(width=32, textvariable=input_web)
inpbox_web.grid(column=1, row=1, sticky='w')  # v3 updated
inpbox_web.focus()
input_mail = tk.StringVar()
inpbox_mail = tk.Entry(textvariable=input_mail)
inpbox_mail.insert(tk.END, 'used_email@gmail.com')
inpbox_mail.grid(column=1, row=2, columnspan=2, sticky=tk.W+tk.E)
input_pswrd = tk.StringVar()
inpbox_pswrd = tk.Entry(width=32, textvariable=input_pswrd)
inpbox_pswrd.grid(column=1, row=3, sticky='w')

# Buttons
bt_password = tk.Button(text='Generate Password', command=new_password)
# bt_password.config(padx=2, pady=2)
bt_password.grid(column=2, row=3, padx=3, pady=3)
# Add to txt row
bt_file = tk.Button(text='Add', command=add_to_file)
bt_file.config(padx=2, pady=2)
bt_file.grid(column=1, row=4, columnspan=2, sticky=tk.W+tk.E)
# Search --- added in v3
# txt
# bt_search = tk.Button(width=13, text='Search', command=search_data_txt)
# json
bt_search = tk.Button(width=13, text='Search', command=search_data_json)
# bt_search.config(padx=2, pady=2)
bt_search.grid(column=2, row=1, padx=3, pady=3)

# END
root.mainloop()
