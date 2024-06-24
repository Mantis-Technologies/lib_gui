#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

"""This contains all the methods from the Find User/Add User page"""

from ..page import Page
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDialog
import re
from lib_keyboard.keyboard import CustomKeyboard
from better_profanity import profanity
from ..Custom_Message_Dialog import ShowCustomMessage


def switch_to_finduseradduser_page(self):
    """Switches to the finduseradduser page"""
    self._switch_to_page(Page.FINDUSERADDUSER)


def handle_skip_button(self):
    """Switches to the next page, the instruction page"""
    # override this function to add additional capability before switching the page
    self.switch_to_instruction_page()


def handle_existing_user_button(self):
    # override this function
    pass


def Get_User_Credentials_From_Existing_User_Input(self) -> {}:
    existing_user_text = self.existing_user_input.text()
    user_credentials = {}

    # Regular expression to check if input is an email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, existing_user_text):
        user_credentials = {"email": existing_user_text}
    else:
        user_credentials = {"username": existing_user_text}
    return user_credentials


def Verify_Existing_User_information(self, email: str, username: str, points: int):
    if email or username:
        print("User found.")
        ShowCustomMessage(self, "The email or username was found.")

        # Display Message Box for 4 seconds before switching
        QTimer.singleShot(4000, self.switch_to_instruction_page)

    else:
        print("User not found.")
        ShowCustomMessage(self, "No user found with the provided email or username.")


def Validate_new_user_input(self) -> {}:
    """Checks if emails match, if they are valid emails, and ensures that the username is not profane.
       Returns username and email if valid."""

    email = self.new_user_email_input.text()
    confirm_email = self.confirm_email_input.text()
    username = self.username_input.text()

    # Email validation regex
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if emails are valid
    if not re.match(email_regex, email):
        ShowCustomMessage(self, "Please enter a valid email address.")
        return None

    # Check if emails match
    if email != confirm_email:
        ShowCustomMessage(self, "The email addresses do not match.")
        return None

    # Check for profanity in the username
    # Initialize the profanity filter
    profanity.load_censor_words()

    # Check for profanity in the username
    if profanity.contains_profanity(username):
        ShowCustomMessage(self, "The username contains inappropriate content.")
        return None
    return {"email": email, "username": username}


def Verify_New_User_information(self, email_exists: bool, username_exists: bool):
    if email_exists:
        ShowCustomMessage(self, "An account with this email already exists.")
        return False

    if username_exists:
        ShowCustomMessage(self, "The username is already taken.")
        return False
    return True


def handle_new_user_button(self):
    # override this function
    pass


def connect_finduseradduser_buttons(self):
    self.skip_button_finduseradduser.clicked.connect(self.handle_skip_button)
    self.existing_user_button.clicked.connect(self.handle_existing_user_button)
    self.new_user_button.clicked.connect(self.handle_new_user_button)


def setup_finduser_adduser_page(self):
    # Get references to widgets
    self.existing_user_input = self.findChild(QLineEdit, 'existingUserInput')
    self.new_user_email_input = self.findChild(QLineEdit, 'newUserEmailInput')
    self.confirm_email_input = self.findChild(QLineEdit, 'confirmEmailInput')
    self.username_input = self.findChild(QLineEdit, 'usernameInput')

    # Connect the text boxes to show the keyboard
    self.existing_user_input.mousePressEvent = lambda event: show_keyboard(self, event, self.existing_user_input)
    self.new_user_email_input.mousePressEvent = lambda event: show_keyboard(self, event, self.new_user_email_input)
    self.confirm_email_input.mousePressEvent = lambda event: show_keyboard(self, event, self.confirm_email_input)
    self.username_input.mousePressEvent = lambda event: show_keyboard(self, event, self.username_input)

    # Connect the skip button to hide the keyboard
    self.skip_button_finduseradduser.clicked.connect(lambda: hide_keyboard_if_exists(self))


def show_keyboard(self, event, target_input):
    if not hasattr(self, 'keyboard'):
        self.keyboard = CustomKeyboard(target_input)
        self.keyboard.enterPressed.connect(self.keyboard.hide)
        self.installEventFilter(self)  # detects clicks outside the keyboard
    else:
        self.keyboard.target_input = target_input

    # Get position of where the QLine edit is, to display keyboard beneath it
    pos = target_input.mapToGlobal(target_input.rect().bottomLeft())
    self.keyboard.move(pos.x(), pos.y())
    self.keyboard.show()


def hide_keyboard_if_exists(self):
    """Hide the keyboard if it exists."""
    if hasattr(self, 'keyboard'):
        self.keyboard.hide_keyboard()


def eventFilter(self, obj, event):
    """Detects mouse click outside of the keyboard and hides keyboard"""
    if event.type() == QEvent.MouseButtonPress:
        if self.keyboard.isVisible() and not self.keyboard.geometry().contains(event.globalPos()):
            self.keyboard.hide()
    return super().eventFilter(obj, event)


def focus_widget(self):
    """Returns which QLineEdit is currently clicked"""
    if self.existing_user_input.hasFocus():
        return self.existing_user_input
    elif self.new_user_email_input.hasFocus():
        return self.new_user_email_input
    elif self.confirm_email_input.hasFocus():
        return self.confirm_email_input
    elif self.username_input.hasFocus():
        return self.username_input
    return None


def clear_text_fields(self):
    """Clear all QLineEdit fields."""
    self.existing_user_input.clear()
    self.new_user_email_input.clear()
    self.confirm_email_input.clear()
    self.username_input.clear()
