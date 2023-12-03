#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to confirmation page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"


from ..page import Page


def switch_to_confirmation_page(self):
    """Switch to confirmation page"""

    self._switch_to_page(Page.CONFIRMATION)


def connect_confirmation_buttons(self):
    """Connects confirmation buttons"""

    self.no_not_21_btn.clicked.connect(self.switch_to_start_page)
    self.yes_over_21_btn.clicked.connect(self.switch_to_payment_page)
