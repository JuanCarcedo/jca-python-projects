"""
    programtester.py
    Control the application.
    Work In Progress
    :copyright: (c) 2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

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
    Control the Login.
    """
    pass


class ProgramTesterApp(App):
    """
    Main class for the app. Inheritance from App required.
    This class controls the movement between screens and parts of
    the app.
    """
    def build(self):
        """
        You should use this one to return the Root Widget.
        return: Class of widget.
        """
        # Create transition between windows
        self.transition = SlideTransition(duration=.4)
        root = ScreenManager(transition=self.transition)

        # Add widgets to main root:
        root.add_widget(LogInWindow(name='login'))
        root.add_widget(UserCreation(name='new_user'))

        return root

    def close_application(self):
        """
        Close the app and close the window.
        """
        App.get_running_app().stop()
        Window.close()


if __name__ == '__main__':
    ProgramTesterApp().run()
