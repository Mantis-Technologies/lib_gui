#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the before proceeding page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney, Nicholas Lanotte"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page


def switch_to_before_proceeding_page(self):
    """Switches to the before proceeding page"""
    self.start_timer_to_ignore_button_presses("Before Proceeding Confirm")
    self._switch_to_page(Page.BEFORE_PROCEEDING)


def before_proceeding_confirm(self):
    if self.check_if_button_is_ok_to_press("Before Proceeding Confirm", 2.0):
        self.switch_to_finduseradduser_page()


def connect_before_proceeding_buttons(self):
    """Connects the before proceeding page next button"""

    self.next_proceeding_btn.clicked.connect(self.before_proceeding_confirm)
    self.cancel_proceeding_btn.clicked.connect(self.switch_to_start_page)
