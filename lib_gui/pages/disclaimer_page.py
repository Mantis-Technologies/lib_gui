#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the disclaimer page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney, Nicholas Lanotte"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page


def switch_to_disclaimer_page(self):
    """Switches to the disclaimer page"""
    self.agree_btn.setEnabled(False)
    self._switch_to_page(Page.DISCLAIMER)


def disclaimer_confirmed(self):
    self.switch_to_confirmation_page()


def connect_disclaimer_buttons(self):
    """Connects the disclaimer page agreed button"""

    self.agree_btn.clicked.connect(self.disclaimer_confirmed)
    self.decline_btn.clicked.connect(self.switch_to_start_page)
