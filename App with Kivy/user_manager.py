"""
    user_manager.py
    Control and manage all user interactions:
        Password, login...
    :copyright: (c) 2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
from db_manager import UserTable
import configuration as config


class UserManager(UserTable):
    """Manage all interactions with security and user."""
    # Users available
    __users_available = []
    # -- Control user entries
    __new_user_status = False
    __new_password_status = False

    def __init__(self):
        super().__init__()
        self.__set_users_available()

    def log_in(self, username: str = None, password: str = None) -> bool:
        """
        Check username and password to access the system.
        :param username: Username ID to check.
        :param password: Password to check.
        :return tuple: False if not granted and True if access granted, message
        """
        # Clear spaces and lower the input.
        username = UserManager.strip_lower_string(username)

        # Check that the fields are not empty.
        if not username or not password:
            return False

        # Only proceed if the user exists:
        if username in self.__get_users_available():
            return True if self.check_login_details_correct(username=username, password=password) else False

        # Default
        return False

    def create_user(self, user_create: str = None, pass_create: str = None, pass_re_entry: str = None) -> bool:
        """
        User validation prior to create a user.
        :param user_create: str. User to be created.
        :param pass_create: str. Password to use.
        :param pass_re_entry: str. Security password re-entry.
        :return: bool. True if all correct, False else.
        """
        # Validate inputs
        if self.validate_user_and_password(method=1, username=user_create,
                                           password=pass_create, re_password=pass_re_entry):
            # Controls in user correct.
            if self.add_data(new_user=UserManager.strip_lower_string(user_create), new_password=pass_create):
                # User created
                self.__set_users_available()
                return True

        # Default to False
        return False

    # Validations
    def perform_checks(self, item_check: str, type_check: int = 0, min_len: int = 7) -> tuple:
        """
        Validation of the parameter "item_check".
        :param item_check: str; username or password
        :param type_check: int; 0 username, 1 password
        :param min_len: int; Minimum length of item_check
        :return: tuple; status, label
        """
        # Default
        status = False
        # Change for username
        item_check = UserManager.strip_lower_string(item_check) if type_check == 0 else item_check

        # Empty or Nothing, directly return
        if not item_check or item_check == '':
            return status, config.STATUS_LABELS[1]

        # Shorter than a minimum
        elif len(item_check) <= min_len:
            label = config.STATUS_LABELS[4]

        # Valid
        else:
            label = config.STATUS_LABELS[2]
            status = True

        # Only for user
        if type_check == 0:
            status = False
            # Longer than a maximum
            if len(item_check) > config.MAX_LEN_USERNAME:
                label = config.STATUS_LABELS[5]

            # Is it available?
            elif self.check_if_user_exists(item_check):
                label = config.STATUS_LABELS[3]

            else:
                status = True

        return status, label

    def validate_user_and_password(self, method: int = 0, username: str = None,
                                   password: str = None, re_password: str = None) -> bool:
        """
        Returns True if the user and password follows the required parameters:
            User and password must be filled *not empty*
            Username must not be already created
            Username and passwords must be over certain length.
            Passwords must be equal
        :param method: int. 0 For user/password, 1 for password/re-password checks.
        :param username: str Username to check.
        :param password: str Password to check.
        :param re_password: str Re-input of password.
        :result str: Code based on type of validation failed. 0 == Correct.
        """
        user_check = self.perform_checks(item_check=username, type_check=0, min_len=config.MIN_LEN_USERNAME)
        pass_check = self.perform_checks(item_check=password, type_check=0, min_len=config.MIN_LEN_PASSWORD)
        if method == 0:
            return True if user_check[0] and pass_check[0] else False

        else:
            # User/ Password and re-password.
            return True if user_check[0] and pass_check[0] and password == re_password else False

    def check_if_user_exists(self, username: str) -> bool:
        """
        Check if the user is in the system.
        :param username: User to search.
        :return bool: True if the user exists, False otherwise.
        """
        return True if username in self.__get_users_available() else False

    # Set and Get properties:
    def __set_users_available(self):
        """Generate users available"""
        self.__users_available = self.gather_users_available()

    def __get_users_available(self) -> list:
        """Return users available"""
        return self.__users_available

    def set_user_status(self, status: bool = False):
        """Set the status of checks for user.
        :param status: Bool. Status to be applied. Default False.
        """
        self.__new_user_status = status

    def get_new_user_status(self):
        """Return the status of new user (if correct or not)."""
        return self.__new_user_status

    def set_password_status(self, status: bool = False):
        """Set the status of checks for password.
        :param status: Bool. Status to be applied. Default False.
        """
        self.__new_password_status = status

    def get_new_password_status(self):
        """Return the status of new password (if correct or not)."""
        return self.__new_password_status

    def clean_status(self):
        """Clean User and Password statuses."""
        self.set_user_status()
        self.set_password_status()

    @staticmethod
    def strip_lower_string(item: str = None) -> str:
        """Do strip and lower to a string. Normally used in user.
        :param item: str. Item to change.
        :return: str. Item changed
        """
        return item.strip().lower()


if __name__ == '__main__':
    print('Note this is meant to be a class only. Do not execute as main.')
