#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the start page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page
from datetime import datetime


def switch_to_start_page(self):
    """Switches to the start page"""

    self._switch_to_page(Page.START)


def OnBeginButtonPressed(self):
    current_time = datetime.now().strftime("%b %d %H:%M:%S")
    message = "Begin Button Pressed"
    # Print message with current time
    print(f"{current_time} : {message}")
    self.switch_to_disclaimer_page()


def connect_start_buttons(self):
    """Connects the start page begin button"""

    self.begin_btn.clicked.connect(self.OnBeginButtonPressed)
    self.about_btn.clicked.connect(self.switch_to_about_page)
