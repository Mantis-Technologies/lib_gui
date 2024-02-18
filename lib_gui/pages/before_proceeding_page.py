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

    self._switch_to_page(Page.BEFORE_PROCEEDING)



def connect_before_proceeding_buttons(self):
    """Connects the before proceeding page next button"""

    self.next_proceeding_btn.clicked.connect(self.switch_to_payment_page)
    self.cancel_proceeding_btn.clicked.connect(self.switch_to_start_page)
