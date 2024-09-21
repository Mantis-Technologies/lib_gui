#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the confirm removal page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney, Nicholas Lanotte"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page


def switch_to_confirm_removal_page(self):
    """Switches to the confirm removal page"""
    self.confirm_removal_btn.setEnabled(False)
    self._switch_to_page(Page.CONFIRM_REMOVAL)


def confirm_removal(self):
    self.switch_to_start_page()

def connect_confirm_removal_buttons(self):
    """Connects the rescan page buttons"""
    self.confirm_removal_btn.clicked.connect(self.confirm_removal)
