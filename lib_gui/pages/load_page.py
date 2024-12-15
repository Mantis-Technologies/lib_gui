#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to loading the sample"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page
from .GetUiDirectoryUtilities import GetCannaCheckUiImagePath
from PySide6.QtGui import QPixmap

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
    loadingGraphicImagePath = GetCannaCheckUiImagePath("CannaCheckKiosk_Sample_Door.png")
    pixmap = QPixmap(loadingGraphicImagePath)  # Replace with the path to your image
    # Set the pixmap to the QLabel
    self.load_sample_graphic.setPixmap(pixmap)

    arrowPath = GetCannaCheckUiImagePath("vecteezy_red-directional-arrow-on-transparent-background_16770572.png")
    pixmap = QPixmap(arrowPath)  # Replace with the path to your image
    # Set the pixmap to the QLabel
    self.load_sample_arrow_png.setPixmap(pixmap)

    self.sample_loaded_btn.clicked.connect(self.finished_load)
    self.cancel_load_btn.clicked.connect(self.cancel_load)
