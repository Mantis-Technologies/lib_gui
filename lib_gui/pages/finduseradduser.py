#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

"""This contains all the methods from the Find User/Add User page"""

from ..page import Page
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox
import re
from lib_keyboard.keyboard import CustomKeyboard
from lib_kiosk.find_user import find_user
from better_profanity import profanity


def switch_to_finduseradduser_page(self):
    """Switches to the finduseradduser page"""
    self._switch_to_page(Page.FINDUSERADDUSER)


def skip_button_finduseradduser(self):
    """Switches to the next page, the instruction page"""
    self.switch_to_instruction_page()


def handle_existing_user_button(self):
    """Sends existing user to find_user function in lib_kiosk, which sends to website to query db"""
    existing_user = self.existing_user_input.text()
    user_credentials = {"email": existing_user}
    email = find_user(user_credentials)
    if email:
        print("User found.")
    else:
        print("User not found.")


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
        QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
        return

    # Check if emails match
    if email != confirm_email:
        QMessageBox.warning(self, "Email Mismatch", "The email addresses do not match.")
        return

    # Check for profanity in the username
    # Initialize the profanity filter
    profanity.load_censor_words()

    # Check for profanity in the username
    if profanity.contains_profanity(username):
        QMessageBox.warning(self, "Invalid Username", "The username contains inappropriate content.")
        return

    QMessageBox.information(self, "Success", "The email and username are valid.")

    # If all checks pass, emit a signal with the email and username
    self.user_data_valid.emit(email, username)

    # Maybe wait for a few seconds before switching
    self.switch_to_instruction_page()


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
    self.skip_button_finduseradduser.clicked.connect(lambda: self.keyboard.hide_keyboard())


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

def eventFilter(self, obj, event):
    if event.type() == QEvent.MouseButtonPress:
        if self.keyboard.isVisible() and not self.keyboard.geometry().contains(event.globalPos()):
            self.keyboard.hide()
    return super().eventFilter(obj, event)


def focus_widget(self):
    if self.existing_user_input.hasFocus():
        return self.existing_user_input
    elif self.new_user_email_input.hasFocus():
        return self.new_user_email_input
    elif self.confirm_email_input.hasFocus():
        return self.confirm_email_input
    elif self.username_input.hasFocus():
        return self.username_input
    return None
