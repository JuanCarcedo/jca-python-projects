"""
    user_management.py
    Control and manage all user interactions:
        Password, login...
    :copyright: (c) 2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
from db_manager import UserTable


class UserManager(UserTable):
    """Manage all interactions with security and user."""

    def __init__(self):
        super().__init__()

    def log_in(self, username: str = None, password: str = None) -> tuple:
        """
        Check username and password to access the system.
        :param username: Username ID to check.
        :param password: Password to check.
        :return tuple: False if not granted and True if access granted, message
        """
        status_check = self.basic_user_password_checks(username, password)
        if status_check[0]:
            if self.check_if_password_correct(status_check[1], status_check[2]):
                # Access to system granted.
                return True, 'Loading access to system...'
            else:
                # Username or password incorrect.
                return False, 'Ups! Username and/or password incorrect.'
        else:
            return False, status_check[3]

    def basic_user_password_checks(self, user_check: str = None, pass_check: str = None) -> tuple:
        """
        Basic checks for the username and password.
        (status, user, password, message)
        :param user_check: Username ID to check.
        :param pass_check: Password to check.
        :return tuple: (status, user, password, message)
            status: False - Something wrong. See message.
            message: Error or success message.
        """

        # (status, user, password, message)
        if user_check is None or pass_check is None:
            return 0, None, None, 'Error; no username or password.'

        # Clear empty spaces and convert to lowercase only in username.
        username = user_check.strip().lower()
        # Passwords are case-sensitive.
        password = pass_check.strip()

        # Check if empty
        if username and password:
            # Check if length is correct:
            if len(username) >= self.MIN_LEN_USERNAME and len(password) >= self.MIN_LEN_PASSWORD:
                return True, username, password, 'Check OK'

            else:
                message = 'Username and/or password too short.'

        else:
            message = 'Username and/or password cannot be empty!'

        return False, username, password, message


if __name__ == '__main__':
    print('Note this is meant to be a class only. Do not execute as main.')
