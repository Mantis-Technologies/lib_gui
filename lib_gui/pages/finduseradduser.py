#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

"""This contains all the methods from the Find User/Add User page"""

from ..page import Page
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox
import re
from lib_keyboard import CustomKeyboard
from lib_kiosk.find_user import find_user
from profanity_check import predict, predict_prob


def switch_to_finduseradduser_page(self):
    """Switches to the finduseradduser page"""
    self._switch_to_page(Page.FINDUSERADDUSER)


def skip_button_finduseradduser(self):
    """Switches to the next page, the instruction page"""
    self.switch_to_instruction_page()


def existing_user_button(self):
    """Sends existing user to find_user function in lib_kiosk, which sends to website to query db"""
    existing_user = self.existing_user_input.text()
    find_user(existing_user)


def new_user_button(self):
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
    if predict([username])[0] == 1:
        QMessageBox.warning(self, "Invalid Username", "The username contains inappropriate content.")
        return

    QMessageBox.information(self, "Success", "The email and username are valid.")

    # If all checks pass, emit a signal with the email and username
    self.user_data_valid.emit(email, username)

    # Maybe wait for a few seconds before switching
    self.switch_to_instruction_page()


def connect_finduseradduser_buttons(self):
    self.instruction_skip.clicked.connect(self.skip_button_finduseradduser)
    self.existing_user_button.clicked.connect(self.existing_user_button)
    self.new_user_button.clicked.connect(self.new_user_button)


def setup_finduser_adduser_page(self):
    # Load UI elements
    loadUi('finduser_adduser.ui', self)

    # Get references to your widgets
    self.existing_user_input = self.findChild(QLineEdit, 'existingUserInput')
    self.new_user_email_input = self.findChild(QLineEdit, 'newUserEmailInput')
    self.confirm_email_input = self.findChild(QLineEdit, 'confirmEmailInput')
    self.username_input = self.findChild(QLineEdit, 'usernameInput')

    # Connect the text boxes to show the keyboard
    self.existing_user_input.mousePressEvent = lambda event: show_keyboard(event, self)
    self.new_user_email_input.mousePressEvent = lambda event: show_keyboard(event, self)
    self.confirm_email_input.mousePressEvent = lambda event: show_keyboard(event, self)
    self.username_input.mousePressEvent = lambda event: show_keyboard(event, self)


def show_keyboard(event, self):
    if not hasattr(self, 'keyboard'):
        self.keyboard = CustomKeyboard(focus_widget(self), self.on_enter_clicked)
        self.keyboard.enterPressed.connect(self.keyboard.hide)
    self.keyboard.show()


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
