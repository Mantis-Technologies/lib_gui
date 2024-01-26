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

    self._switch_to_page(Page.RESCAN_RESULTS)



def connect_rescan_buttons(self):
    """Connects the rescan page buttons"""

    self.cancel_test_btn.clicked.connect(self.switch_to_start_page)
    self.rescan_btn.clicked.connect(self.switch_to_load_page)
    self.view_results_btn.clicked.connect(self.switch_to_results_page)