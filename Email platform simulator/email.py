"""
    email
    Email class.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""


class Email:
    def __init__(self, sender_address: str, email_body: str = ''):
        self.from_address = sender_address
        self.email_contents = email_body
        # Set the following private variables to False.
        # User cannot directly access them.
        self.__has_been_read = False
        self.__is_spam = False

    def mark_as_read(self):
        self.__has_been_read = True

    def mark_as_spam(self):
        self.__is_spam = True

    def check_read_status(self):
        # Retrieve the status of read.
        return self.__has_been_read

    def check_spam_status(self):
        # Retrieve the status of spam.
        return self.__is_spam
