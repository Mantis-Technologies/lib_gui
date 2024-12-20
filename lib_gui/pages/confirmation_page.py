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

    self.yes_over_21_btn.setEnabled(False)
    self._switch_to_page(Page.CONFIRMATION)


def over_21_confirm(self):
    self.switch_to_before_proceeding_page()


def connect_confirmation_buttons(self):
    """Connects confirmation buttons"""

    self.no_not_21_btn.clicked.connect(self.switch_to_start_page)
    self.yes_over_21_btn.clicked.connect(self.over_21_confirm)
