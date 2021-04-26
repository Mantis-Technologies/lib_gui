#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the scanning page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page


def switch_to_scanning_page(self):
    """Move to scanning page"""

    self._switch_to_page(Page.SCANNING)
