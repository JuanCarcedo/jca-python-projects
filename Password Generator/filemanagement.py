"""
    filemanagement.py
    Controls the flow between the program and the files.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
import json
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno

JSON_FILE = 'data.json'


def create_file_json(mail, password, web):
    """
    Generate a json file with the data or update the current one.
    :param str mail: Email to be used
    :param str password: Password to be used
    :param str web: Webpage to store the email and password
    :return: None
    """
    new_data = {
        web: {
            "username": mail,
            "pass": password
        }
    }
    try:  # Error if file does not exist
        with open(JSON_FILE, mode='r') as file:
            data_json = json.load(file)
    except FileNotFoundError:
        with open(JSON_FILE, mode='w') as file:
            json.dump(new_data, file, indent=2)
    else:
        data_json.update(new_data)
        with open(JSON_FILE, mode='w') as file:
            json.dump(data_json, file, indent=2)


def add_to_file(mail=None, password=None, web=None) -> bool:
    """
    Check parameters before sending to file.
    :param str mail: Email to be used
    :param str password: Password to be used
    :param str web: Webpage to store the email and password
    :return: True if the file was updated else False
    """
    if not mail or not password or not web:
        pop_up(title='Warning',
               message='Empty fields.',
               type_mess='warning')
    else:  # All fields filled
        review_ok = pop_up(title='Review fields',
                           message=f'Email: {mail}\n Password: {password}\n is this ok?',
                           type_mess='yesno')
        if review_ok:
            create_file_json(mail=mail,
                             password=password,
                             web=web)
            return True
    return False


def search_data_json(web_search=None):
    """
    Search the Website and username in the db
    :param web_search: Web to search
    :return: Username and password if found (json)
    """
    if web_search:  # not empty
        try:
            with open(JSON_FILE) as file:
                json_data = json.load(file)
        except FileNotFoundError:
            pop_up(title='Error',
                   message='No file with data found.',
                   type_mess='error')
        else:
            if web_search in json_data:  # Key in there
                text = f"Username: {json_data[web_search]['username']}" \
                       f"\nPassword: {json_data[web_search]['pass']}"
            else:
                text = f"No data for {web_search}"
            pop_up(title='Search result',
                   message=text,
                   type_mess='info')
    else:
        pop_up(title='Warning',
               message='Website is empty.',
               type_mess='warning')


def pop_up(title: str = '', message: str = '', type_mess: str = ''):
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
