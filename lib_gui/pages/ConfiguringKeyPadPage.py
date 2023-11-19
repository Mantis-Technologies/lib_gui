#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the configure keypad page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page


def switch_to_ConfiguringKeyPad_page(self):
    """Switches to the results page"""

    self._switch_to_page(Page.KEYPAD)