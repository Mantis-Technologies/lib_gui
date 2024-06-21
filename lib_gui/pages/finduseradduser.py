#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

"""This contains all the methods from the Find User/Add User page"""

from ..page import Page
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDialog
import re
from lib_keyboard.keyboard import CustomKeyboard
from lib_kiosk.find_user import find_user
from lib_kiosk.check_new_user import check_new_user
from better_profanity import profanity


# Subclass for QMessage boxes
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, Qt

class CustomMessageBox(QMessageBox):
    def __init__(self, parent=None, *args, **kwargs):
        super(CustomMessageBox, self).__init__(parent, *args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)

        # print("CustomMessageBox created")  # Debug print

        # Set a timer to close the message box after 4 seconds (4000 milliseconds)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.handle_close)
        self.timer.start(4000)
        # print("Timer started for 4 seconds")  # Debug print

        # Ensure the message box appears in front
        self.raise_()
        self.activateWindow()

        # Remove default buttons
        self.setStandardButtons(QMessageBox.NoButton)

    def showEvent(self, event):
        super(CustomMessageBox, self).showEvent(event)
        # print("CustomMessageBox shown")  # Debug print

    def handle_close(self):
        # print("Handling CustomMessageBox close")  # Debug print
        self.accept()  # Close the message box


def switch_to_finduseradduser_page(self):
    """Switches to the finduseradduser page"""
    self._switch_to_page(Page.FINDUSERADDUSER)


def skip_button_finduseradduser(self):
    """Switches to the next page, the instruction page"""
    self.clear_user_data()  # Clear the user data so the previous user is not sent the results
    self.switch_to_instruction_page()


def handle_existing_user_button(self):
    """Sends existing user to find_user function in lib_kiosk, which sends to website to query db"""
    existing_user_text = self.existing_user_input.text()
    user_credentials = {}

    # Regular expression to check if input is an email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, existing_user_text):
        user_credentials = {"email": existing_user_text}
    else:
        user_credentials = {"username": existing_user_text}

    email, username, points = find_user(user_credentials)

    if email or username:
        print("User found.")
        msg_box = CustomMessageBox(self)
        msg_box.setText("The email or username was found.")
        msg_box.show()
        self.user_data_valid.emit(email, username, points)

        # Maybe wait for a few seconds before switching
        QTimer.singleShot(4000, self.switch_to_instruction_page)

    else:
        print("User not found.")
        msg_box = CustomMessageBox(self)
        msg_box.setText("No user found with the provided email or username.")
        msg_box.show()

def handle_new_user_button(self):
    """Checks if emails match, if they are valid emails, and ensures that the username is not profane.
    Returns username and email if valid."""

    email = self.new_user_email_input.text()
    confirm_email = self.confirm_email_input.text()
    username = self.username_input.text()

    # Email validation regex
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if emails are valid
    if not re.match(email_regex, email):
        msg_box = CustomMessageBox(self)
        msg_box.setText("Please enter a valid email address.")
        msg_box.show()
        return

    # Check if emails match
    if email != confirm_email:
        msg_box = CustomMessageBox(self)
        msg_box.setText("The email addresses do not match.")
        msg_box.show()
        return

    # Check for profanity in the username
    # Initialize the profanity filter
    profanity.load_censor_words()

    # Check for profanity in the username
    if profanity.contains_profanity(username):
        msg_box = CustomMessageBox(self)
        msg_box.setText("The username contains inappropriate content.")
        msg_box.show()
        return

    # Check if email or username already exists
    # Check if email or username already exists
    user_credentials = {"email": email, "username": username}
    email_exists, username_exists = check_new_user(user_credentials)

    if email_exists:
        msg_box = CustomMessageBox(self)
        msg_box.setText("An account with this email already exists.")
        msg_box.show()
        return

    if username_exists:
        msg_box = CustomMessageBox(self)
        msg_box.setText("The username is already taken.")
        msg_box.show()
        return

    msg_box = CustomMessageBox(self)
    msg_box.setText("The email and username are valid.")
    msg_box.show()

    # If all checks pass, emit a signal with the email and username
    self.user_data_valid.emit(email, username)

    # Maybe wait for a few seconds before switching
    QTimer.singleShot(4000, self.switch_to_instruction_page)


def connect_finduseradduser_buttons(self):
    self.skip_button_finduseradduser.clicked.connect(self.switch_to_instruction_page)
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
        self.installEventFilter(self) # detects clicks outside the keyboard
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
