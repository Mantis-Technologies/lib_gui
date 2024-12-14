#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

"""This contains all the methods from the Find User/Add User page"""

from ..page import Page
from PySide6.QtCore import Qt, QEvent, QTimer, QObject
from PySide6.QtWidgets import QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDialog
import re
from lib_keyboard.keyboard import CustomKeyboard
from better_profanity import profanity
from .GetUiDirectoryUtilities import GetCannaCheckUiImagePath
from PySide6.QtGui import QPixmap

def switch_to_finduseradduser_page(self):
    """Switches to the finduseradduser page"""
    self._switch_to_page(Page.FINDUSERADDUSER)


def handle_skip_button(self):
    """Switches to the next page, the instruction page"""
    self.hide_keyboard_if_exists()
    # override this function to add additional capability before switching the page
    self.switch_to_payment_page()


def handle_existing_user_button(self):
    # override this function
    pass


def Get_User_Credentials_From_Existing_User_Input(self) -> {}:
    existing_user_text = self.newUserEmailInput.text()
    user_pin = self.user_pin_entry.text()
    user_credentials = {}

    # Regular expression to check if input is an email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, existing_user_text):
        user_credentials = {"email": existing_user_text, "pin": user_pin}
    else:
        user_credentials = {"username": existing_user_text, "pin": user_pin}
    return user_credentials


def Validate_new_user_input(self) -> ({}, str):
    """Checks if emails match, if they are valid emails, and ensures that the username is not profane.
       Returns username and email if valid."""

    email = self.newUserEmailInput.text()
    confirm_email = self.confirmEmailInput.text()
    username = self.usernameInput.text()

    # Email validation regex
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if emails are valid
    if not re.match(email_regex, email):
        return {}, "Please enter a valid email address."

    # Check if emails match
    if email != confirm_email:
        return {}, "The email addresses do not match."

    # Check for profanity in the username
    # Initialize the profanity filter
    profanity.load_censor_words()

    # Check for profanity in the username
    if profanity.contains_profanity(username):
        return {}, "The username contains inappropriate content."
    return {"email": email, "username": username}, ""


def Verify_New_User_information(self, email_exists: bool, username_exists: bool) -> (bool, str):
    if email_exists:
        return False, "An account with this email already exists."

    if username_exists:
        return False, "The username is already taken."
    return True, ""


def handle_new_user_button(self):
    # override this function
    pass


def connect_finduseradduser_buttons(self):
    self.skip_button_finduseradduser.clicked.connect(self.handle_skip_button)
    self.existing_user_button.clicked.connect(self.handle_existing_user_button)
    self.new_user_button.clicked.connect(self.handle_new_user_button)

    roundedSquarePath = GetCannaCheckUiImagePath("green_shape (3000 x 3000 px).png")
    pixmap = QPixmap(roundedSquarePath)  # Replace with the path to your image
    # Set the pixmap to the QLabel
    self.green_rounded_square_png.setPixmap(pixmap)

def setup_finduser_adduser_page(self):
    # Set echo mode to Password to hide the PIN entry behind asterisks
    self.user_pin_entry.setEchoMode(QLineEdit.Password)

    # Connect the text boxes to show the keyboard
    self.existingUserInput.mousePressEvent = lambda event: (show_keyboard(self, event, self.existingUserInput), QLineEdit.mousePressEvent(self.existingUserInput, event))
    self.user_pin_entry.mousePressEvent = lambda event: (show_keyboard(self, event, self.user_pin_entry), QLineEdit.mousePressEvent(self.user_pin_entry, event))
    self.newUserEmailInput.mousePressEvent = lambda event: (show_keyboard(self, event, self.newUserEmailInput), QLineEdit.mousePressEvent(self.newUserEmailInput, event))
    self.confirmEmailInput.mousePressEvent = lambda event: (show_keyboard(self, event, self.confirmEmailInput), QLineEdit.mousePressEvent(self.confirmEmailInput, event))
    self.usernameInput.mousePressEvent = lambda event: (show_keyboard(self, event, self.usernameInput), QLineEdit.mousePressEvent(self.usernameInput, event))


def show_keyboard(self, event, target_input):
    if not hasattr(self, 'keyboard'):
        self.keyboard = CustomKeyboard(target_input, self.centralWidget())
        self.keyboard.enterPressed.connect(self.keyboard.hide)
        #self.installEventFilter(self)  # detects clicks outside the keyboard
    else:
        self.keyboard.target_input = target_input

    # Get position of where the QLine edit is, to display keyboard beneath it

    pos = target_input.mapToParent(target_input.rect().bottomLeft())
    self.keyboard.move(pos.x(), pos.y())
    self.keyboard.show()


def hide_keyboard_if_exists(self):
    """Hide the keyboard if it exists."""
    if hasattr(self, 'keyboard'):
        self.keyboard.hide_keyboard()


def focus_widget(self):
    """Returns which QLineEdit is currently clicked"""
    if self.existingUserInput.hasFocus():
        return self.existingUserInput
    elif self.user_pin_entry.hasFocus():
        return self.user_pin_entry
    elif self.newUserEmailInput.hasFocus():
        return self.newUserEmailInput
    elif self.confirmEmailInput.hasFocus():
        return self.confirmEmailInput
    elif self.usernameInput.hasFocus():
        return self.usernameInput
    return None


def clear_text_fields(self):
    """Clear all QLineEdit fields."""
    self.existingUserInput.clear()
    self.user_pin_entry.clear()
    self.newUserEmailInput.clear()
    self.confirmEmailInput.clear()
    self.usernameInput.clear()
