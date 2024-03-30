#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the maintenaince page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page


def switch_to_maintenance_page(self):
    """Switches to the results page"""
    self._switch_to_page(Page.MAINTENANCE)


def connect_maintenance_buttons(self):
    self.exitMainenanceBtn.clicked.connect(self.switch_to_start_page)
    self.EjectSampleBtn.clicked.connect(self.MoveToEject)
    self.ResetSampleBtn.clicked.connect(self.HomeMotionSystem)
    self.PrintLastReceiptBtn.clicked.connect(self.PrintLastReceipt)


def HomeMotionSystem(self):
    pass  # override me


def MoveToEject(self):
    pass  # override me


def PrintLastReceipt(self):
    pass  # override me
