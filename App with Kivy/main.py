"""
    main.py
    App to control multiple programs with Python.
    TODO:
        - Create user: Size with the inputs.
        - When going back to log in, delete the field.
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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
# Other imports
import configuration as config
from user_manager import UserManager


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
    """Control the user creation screen."""
    # Kivy properties.
    new_user = ObjectProperty(None)
    new_password = ObjectProperty(None)
    repeat_password = ObjectProperty(None)  # Re-check for password.
    #  Text attributes:
    label_check_username = StringProperty()
    label_check_password = StringProperty()
    label_check_repeat_password = StringProperty()

    def __init__(self, **kwargs):
        super(UserCreation, self).__init__(**kwargs)
        # Default labels for checks
        self.set_label_check_user(config.STATUS_LABELS[1])
        self.set_label_check_password(config.STATUS_LABELS[1])
        self.set_label_check_repeat_password(config.STATUS_LABELS[1])

    def create_new_user(self):
        """ Send username and password to the database. """
        # Note create new user always validate.
        if user_manager.create_user(user_create=self.new_user.text,
                                    pass_create=self.new_password.text,
                                    pass_re_entry=self.repeat_password.text):
            # Pop up with confirmation:
            ProgramTesterApp.pop_ups_generator(title_pop='New User', text_pop='User Created!')
            self.go_back_login()

        else:
            # Something went wrong.
            # Pop up:
            ProgramTesterApp.pop_ups_generator(title_pop='Warning', text_pop='User not created, check parameters.')

    def validate_username(self) -> None:
        """ On the fly validation of user.
            User must be unique (not exists), longer than X chars and not being empty.
        """
        # Reduce errors: Clear empty spaces in username and put it in lower.
        validation = user_manager.perform_checks(
            item_check=self.new_user.text, type_check=0, min_len=config.MIN_LEN_USERNAME)
        user_manager.set_user_status(validation[0])
        self.set_label_check_user(validation[1])

    def validate_password(self) -> None:
        """ On the fly validation of passwords.
            Password must be longer than X chars and not being empty.
            Password and re-entering must be equal.
        """
        # Password
        password_check = user_manager.perform_checks(
            item_check=self.new_password.text, type_check=1, min_len=config.MIN_LEN_PASSWORD)

        user_manager.set_password_status(password_check[0])
        self.set_label_check_password(password_check[1])

        # Passwords equal?
        if self.repeat_password.text != self.new_password.text:
            re_enter_password_check = config.STATUS_LABELS[6]
            user_manager.set_password_status(password_check[0])

        else:
            # Re enter password
            _, re_enter_password_check = user_manager.perform_checks(
                item_check=self.repeat_password.text, type_check=1, min_len=config.MIN_LEN_PASSWORD)

        self.set_label_check_repeat_password(re_enter_password_check)

    # Button
    def go_back_login(self):
        """Go back to log in (always will clean the fields)."""
        self.__clean_fields()
        # Change transition
        self.manager.transition.direction = 'left'
        # Change screen to home/menu
        self.manager.current = 'login'

    # Other methods
    def set_label_check_user(self, text: str = ''):
        """Set the value of username check label"""
        self.label_check_username = text

    def set_label_check_password(self, text: str = ''):
        """Set the value of password check label"""
        self.label_check_password = text

    def set_label_check_repeat_password(self, text: str = ''):
        """Set the value of repeat password check label"""
        self.label_check_repeat_password = text

    def __clean_fields(self):
        """Clear login fields."""
        self.set_label_check_user(config.STATUS_LABELS[0])
        self.set_label_check_password(config.STATUS_LABELS[0])
        self.set_label_check_repeat_password(config.STATUS_LABELS[0])
        self.new_user.text, self.new_password.text, self.repeat_password.text = '', '', ''
        user_manager.clean_status()


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
        if user_manager.log_in(username=self.user_id.text, password=self.user_password.text):
            # Pop up with confirmation:
            ProgramTesterApp.pop_ups_generator(title_pop='Log In', text_pop='Success! Welcome')

            self.clear_fields()
            # Change transition
            self.manager.transition.direction = 'left'
            # Change screen to home/menu
            self.manager.current = 'menu'

        else:
            # Incorrect details
            self.message_to_users = 'Wrong details.'

    def clear_fields(self):
        """Clear all fields."""
        self.user_id.text, self.user_password.text, self.message_to_users = '', '', ''


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
        """Close the app and close the window."""
        App.get_running_app().stop()
        Window.close()

    @staticmethod
    def pop_ups_generator(title_pop: str = 'Ups', text_pop: str = 'Nothing shared.'):
        """ Control pop-ups.
        :param title_pop: str. Title for the pop-up.
        :param text_pop: str. Text inside the pop-up.
        """
        popup_item = Popup(title=title_pop,
                           title_align='center',
                           content=Label(text=text_pop,
                                         text_size=(100, None),
                                         halign='center', valign='middle'),
                           size_hint=(None, None), size=(200, 200))
        popup_item.open()


if __name__ == '__main__':
    user_manager = UserManager()  # Management to User access
    ProgramTesterApp().run()  # App
