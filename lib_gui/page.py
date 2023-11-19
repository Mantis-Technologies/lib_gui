#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from enum import Enum


class Page(Enum):
    """Contains the page order of the stackedWidget"""

    BOOTING = 0
    START = 1
    # Over 21 page
    CONFIRMATION = 2
    ORDER = 3
    LOAD = 4
    SCANNING = 5
    RESULTS = 6
    ERROR = 7
    PAYMENT = 8
    KEYPAD = 9
