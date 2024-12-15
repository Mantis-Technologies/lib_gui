#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the before proceeding page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney, Nicholas Lanotte"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page
from .GetUiDirectoryUtilities import GetCannaCheckUiImagePath
from PySide6.QtGui import QPixmap

def switch_to_before_proceeding_page(self):
    """Switches to the before proceeding page"""
    self.next_proceeding_btn.setEnabled(False)
    self._switch_to_page(Page.BEFORE_PROCEEDING)


def before_proceeding_confirm(self):
    self.switch_to_finduseradduser_page()


def connect_before_proceeding_buttons(self):
    """Connects the before proceeding page next button"""

    self.next_proceeding_btn.clicked.connect(self.before_proceeding_confirm)
    self.cancel_proceeding_btn.clicked.connect(self.switch_to_start_page)

    happyNugPath = GetCannaCheckUiImagePath("happy_nug_transparent.png")
    pixmap = QPixmap(happyNugPath)  # Replace with the path to your image
    # Set the pixmap to the QLabel
    self.happy_nug.setPixmap(pixmap)

    grinderPath = GetCannaCheckUiImagePath("grinder_transparent.png")
    pixmap = QPixmap(grinderPath)  # Replace with the path to your image
    # Set the pixmap to the QLabel
    self.grinder.setPixmap(pixmap)

    petriDishPath = GetCannaCheckUiImagePath("petri_dish_transparent.png")
    pixmap = QPixmap(petriDishPath)  # Replace with the path to your image
    # Set the pixmap to the QLabel
    self.petri_dish.setPixmap(pixmap)
