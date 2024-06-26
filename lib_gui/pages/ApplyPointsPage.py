#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the apply points page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page


def switch_to_ApplyPointsPage(self):
    """Switch to confirmation page"""

    self._switch_to_page(Page.APPLYPOINTS)


def connect_ApplyPointsPage_buttons(self):
    """Connects the before proceeding page next button"""

    self.Confirm_Apply_Points.clicked.connect(self.Confirm_PointsApplied)
    self.skip_button_apply_points.clicked.connect(self.Skip_PointsApplied)


def Confirm_PointsApplied(self):
    self._switch_to_page(Page.INSTRUCTIONS)


def Skip_PointsApplied(self):
    self._switch_to_page(Page.INSTRUCTIONS)