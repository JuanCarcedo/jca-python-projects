"""
    main.py
    App to control multiple programs with Python.
    TODO:
        - Create user: Size with the inputs.
        - Solve issue with message to users when jumping between screens.
        - Menu
    Work In Progress:
    - Access to system: Ok
    - Create new user: 80% - Style left.
    - Menu: WIP
    - Game 1: WIP
    :copyright: (c) 2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
# Kivy APP imports
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
# Other imports
import configuration as config
from user_management import UserManager


# CONSTANTS or Requirements
kivy.require('2.1.0')  # kivy requirement
# Windows minimum parameters:
Window.minimum_height, Window.minimum_width = (config.MINIMUM_HEIGHT, config.MINIMUM_WIDTH)


class Menu(Screen):
    """ Home. Landing page after log in correct."""
    # Kivy properties.

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)


class UserCreation(Screen):
    """Control the user creation."""
    # Kivy properties.
    new_user = ObjectProperty(None)
    new_password = ObjectProperty(None)
    repeat_password = ObjectProperty(None)  # Re-check for password.
    #  Text attributes:
    label_check_username = StringProperty()
    label_check_password = StringProperty()
    label_check_repeat_password = StringProperty()
    # Class properties
    # -- Control user entries
    user_status = False
    password_status = False

    def __init__(self, **kwargs):
        super(UserCreation, self).__init__(**kwargs)
        # Default labels for checks
        self.label_check_username = config.STATUS_LABELS[1]
        self.label_check_password = config.STATUS_LABELS[1]
        self.label_check_repeat_password = config.STATUS_LABELS[1]

    def create_new_user(self):
        """ Send username and password to the database. """
        # Note create new user always validate.
        if UserCreation.validate_user_and_password(username=self.new_user.text,
                                                   password=self.new_password.text,
                                                   re_password=self.repeat_password.text):
            # Checks OK
            if user_manager.add_data(new_user=self.new_user.text, new_password=self.new_password.text):
                # Change screen to log-in
                self.manager.current = 'login'

    def __perform_checks(self, item_check: str,
                         type_check: int = 0,
                         min_len: int = 7) -> tuple:
        """
        Validation of the parameter "item_check".
        :param item_check: str; username or password
        :param type_check: int; 0 username, 1 password
        :param min_len: int; Minimum length of item_check
        :return: tuple; status, label
        """
        # Default
        status = False

        # Empty
        if not item_check:
            label = config.STATUS_LABELS[1]

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
            elif user_manager.check_if_user_exists(item_check):
                label = config.STATUS_LABELS[3]

            else:
                status = True

        return status, label

    def validate_username(self) -> None:
        """ On the fly validation of user.
            User must be unique (not exists), longer than X chars and not being empty.
        """
        # Reduce errors: Clear empty spaces in username and put it in lower.
        self.user_status, self.label_check_username = self.__perform_checks(
            item_check=self.new_user.text.strip().lower(),
            type_check=0,
            min_len=config.MIN_LEN_USERNAME)

    def validate_password(self) -> None:
        """ On the fly validation of passwords.
            Password must be longer than X chars and not being empty.
            Password and re-entering must be equal.
        """
        # Password
        self.password_status, self.label_check_password = self.__perform_checks(
            item_check=self.new_password.text,
            type_check=1,
            min_len=config.MIN_LEN_PASSWORD)

        # Re enter password
        _, self.label_check_repeat_password = self.__perform_checks(
            item_check=self.repeat_password.text,
            type_check=1,
            min_len=config.MIN_LEN_PASSWORD)

        # Passwords equal?
        if self.repeat_password.text != self.new_password.text:
            self.label_check_repeat_password = config.STATUS_LABELS[6]
            self.password_status = False

    @staticmethod
    def validate_user_and_password(username: str = None, password: str = None, re_password: str = None) -> bool:
        """  -- Available for other methods  --
        Returns True if the user and password follows the required parameters:
            User and password must be filled *not empty*
            Username must not be already created
            Username and passwords must be over certain length.
            Passwords must be equal
        :param username: str Username to check.
        :param password: str Password to check.
        :param re_password: str Re-input of password.
        :result str: Code based on type of validation failed. 0 == Correct.
        """
        # Reduce errors: Clear empty spaces in username and put in lower.
        username = username.strip().lower()
        # Username and Password are not empty
        if not username or not password:
            return False
        # Username already exists:
        if user_manager.check_if_user_exists(username):
            return False
        # Constraint in length:
        if len(username) <= config.MIN_LEN_USERNAME:
            return False
        if len(password) <= config.MIN_LEN_PASSWORD:
            return False
        # Passwords equal:
        if password != re_password:
            return False

        # All conditions passed
        return True


class LogInWindow(Screen):
    """ Login control."""
    # Kivy properties.
    user_id = ObjectProperty(None)
    user_password = ObjectProperty(None)
    message_to_users = StringProperty()  # Warning messages.

    def __init__(self, **kwargs):
        super(LogInWindow, self).__init__(**kwargs)

    # Log into system checks/methods
    def show_hide_password(self, selection: int = 0) -> None:
        """
        Show or hide the password.
        :param selection: 0 Hide password, 1 show it.
        :return: None.
        """
        self.user_password.password = False if selection == 1 else True

    def check_log_in(self) -> None:
        """Manage log into the system."""
        if user_manager.check_login_details_correct(username=self.user_id.text, password=self.user_password.text):
            # Change transition
            self.manager.transition.direction = 'left'
            # Change screen to home/menu
            self.manager.current = 'menu'

        else:
            # Incorrect details
            self.message_to_users = 'Wrong details.'


class ProgramTesterApp(App):
    """
    Main class for the app. Inheritance from App required.
    This class controls the movement between screens and parts of
    the app.
    """
    def build(self):
        """
        You should use this one to return the Root Widget.
        Note that all Widgets MUST be included here.
        return: Class of widget.
        """
        # Widget(s) included in App ============================
        # New widgets must be included here.
        self.login_to_system = LogInWindow(name='login')
        self.new_user = UserCreation(name='new_user')
        self.menu = Menu(name='menu')
        # ===================================================

        # Create transition between windows
        self.transition = SlideTransition(duration=.4)
        root = ScreenManager(transition=self.transition)

        # Add widgets to main root:
        root.add_widget(self.login_to_system)  # Log in page
        # New widgets must be included below:
        root.add_widget(self.new_user)  # Creation of users
        root.add_widget(self.menu)  # App landing page when log in

        return root

    def close_application(self):
        """
        Close the app and close the window.
        """
        App.get_running_app().stop()
        Window.close()


if __name__ == '__main__':
    user_manager = UserManager()  # Management to User access
    ProgramTesterApp().run()  # App
