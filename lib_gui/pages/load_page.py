#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to loading the sample"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page


def switch_to_load_page(self):
    """Switches to load page"""
    self.sample_loaded_btn.setEnabled(False) # disable this button until the slide has ejected
    self._switch_to_page(Page.LOAD)



def cancel_load(self):
    """Cancels load and moves to start page"""

    self.switch_to_start_page()


def finished_load(self):
    """Load is complete, move to scanning page"""
    self.switch_to_scanning_page()


def connect_load_buttons(self):
    """Connects load buttons"""

    self.sample_loaded_btn.clicked.connect(self.finished_load)
    self.cancel_load_btn.clicked.connect(self.cancel_load)
