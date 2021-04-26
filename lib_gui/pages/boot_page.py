#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all boot page methods"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"


from ..page import Page


def switch_to_boot_page(self):
    """Switches to boot page"""

    self._switch_to_page(Page.BOOTING)
