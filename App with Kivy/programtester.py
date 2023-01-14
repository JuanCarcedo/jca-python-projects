"""
    programtester.py
    App to control multiple programs with Python.
    Work In Progress:
    - Access to system: Ok
    - Create new user: WIP
    - First application with UI: WIP
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
from user_management import UserManager


# CONSTANTS or Requirements
kivy.require('2.1.0')  # kivy requirement
# Windows minimum parameters:
Window.minimum_height, Window.minimum_width = (500, 400)


class UserCreation(Screen):
    """Control the user creation."""
    # Kivy properties.
    new_user_id = ObjectProperty(None)
    new_user_password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UserCreation, self).__init__(**kwargs)

    def create_new_user(self):
        pass


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

    def check_log_in(self):
        """Manage log into the system."""
        status_login = user_manager.log_in(self.user_id.text, self.user_password.text)
        self.message_to_users = status_login[1]


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
        # ===================================================

        # Create transition between windows
        self.transition = SlideTransition(duration=.4)
        root = ScreenManager(transition=self.transition)

        # Add widgets to main root:
        # New widgets must be included here.
        root.add_widget(self.login_to_system)  # LogInWindow(name='login'))
        root.add_widget(self.new_user)  # UserCreation(name='new_user'))

        return root

    def close_application(self):
        """
        Close the app and close the window.
        """
        App.get_running_app().stop()
        Window.close()


if __name__ == '__main__':
    user_manager = UserManager()
    ProgramTesterApp().run()  # App
