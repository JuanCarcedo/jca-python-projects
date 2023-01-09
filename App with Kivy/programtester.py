"""
    programtester.py
    Control the application.
    Work In Progress
    :copyright: (c) 2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
# Kivy APP imports
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
# Other imports
from db_manager import UserTable


# CONSTANTS or Requirements
kivy.require('2.1.0')  # kivy requirement
# Windows minimum parameters:
Window.minimum_height, Window.minimum_width = (500, 400)


class UserCreation(Screen):
    """
    Control the user creation.
    """
    pass


class LogInWindow(Screen):
    """
    Login control.
    """

    def __init__(self, **kwargs):
        super(LogInWindow, self).__init__(**kwargs)
        # User database table
        self.user_db = UserTable()

    def log_in_check(self, user, password):
        # TO-DO: Implement check that user and password are not empty.

        if self.user_db.check_if_password_correct(user, password):
            # Access to system granted.
            pass
        else:
            # Username or password incorrect.
            message = 'Ups! Username and/or password incorrect.'


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
        self.login_to_system = LogInWindow(name='login')
        self.new_user = UserCreation(name='new_user')
        # ===================================================

        # Create transition between windows
        self.transition = SlideTransition(duration=.4)
        root = ScreenManager(transition=self.transition)

        # Add widgets to main root:
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
    ProgramTesterApp().run()
