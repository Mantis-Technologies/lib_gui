#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the scanning page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page
from .GetUiDirectoryUtilities import GetCannaCheckUiImagePath
from PySide6.QtGui import QPixmap
def Load_Pixmaps_Scanning_Page(self):
    testTubePath = GetCannaCheckUiImagePath("test_tube_tansparent.png")
    pixmap = QPixmap(testTubePath)  # Replace with the path to your image

    # Set the pixmap to the QLabel
    self.test_tube.setPixmap(pixmap)

def switch_to_scanning_page(self):
    """Move to scanning page"""

    self._switch_to_page(Page.SCANNING)
