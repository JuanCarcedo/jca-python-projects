"""
    filemanagement.py
    Controls the flow between the program and the files.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
import json


class JsonFileManager:
    JSON_FILE = 'data.json'

    def create_file_json(self, mail, password, web) -> bool:
        """
        Generate a json file with the data or update the current one.
        :param str mail: Email to be used
        :param str password: Password to be used
        :param str web: Webpage to store the email and password
        :return: bool. True if all correct. False otherwise.
        """
        new_data = {
            web: {
                "username": mail,
                "pass": password
            }
        }
        try:  # Error if file does not exist
            with open(self.get_json_file(), mode='r') as file:
                data_json = json.load(file)

        except FileNotFoundError:
            with open(self.get_json_file(), mode='w') as file:
                json.dump(new_data, file, indent=2)
            return False

        else:
            data_json.update(new_data)
            with open(self.get_json_file(), mode='w') as file:
                json.dump(data_json, file, indent=2)

        return True

    def search_data_json(self, web_search: str = None) -> tuple:
        """
        Search the Website and username in the db
        :param web_search: str. Web to search
        :return: tuple. (title_popup, message_popup, type_message_popup)
        """
        try:
            with open(self.get_json_file()) as file:
                json_data = json.load(file)
        except FileNotFoundError:
            return 'Error', 'No file with data found.', 'error', None
        else:
            if web_search in json_data:  # Key in there
                password = json_data[web_search]['pass']
                text = f"Username: {json_data[web_search]['username']}" \
                       f"\nPassword: {password}"

            else:
                text = f"No data for {web_search}"
                password = None

            return 'Search result', text, 'info', password

    def get_json_file(self):
        """Retrieve the value of the json file."""
        return self.JSON_FILE


if __name__ == '__main__':
    print('I am not supposed to be the main...')
