#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the rescan page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney, Nicholas Lanotte"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page


def switch_to_rescan_page(self):
    """Switches to the rescan page"""
    self.cancel_test_btn.setEnabled(False)
    self.rescan_btn.setEnabled(False)
    self.view_results_btn.setEnabled(False)
    self._switch_to_page(Page.RESCAN_RESULTS)


def on_cancel_test(self):
    self.switch_to_confirm_removal_page()


def on_rescan_test(self):
    self.switch_to_load_page()


def on_see_results(self):
    self.switch_to_results_page()


def connect_rescan_buttons(self):
    """Connects the rescan page buttons"""

    self.cancel_test_btn.clicked.connect(self.on_cancel_test)
    self.rescan_btn.clicked.connect(self.on_rescan_test)
    self.view_results_btn.clicked.connect(self.on_see_results)
