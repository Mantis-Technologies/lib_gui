#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page


def switch_to_Network_Outage_page(self):
    """Switches to the about page"""
    self._switch_to_page(Page.NETWORKOUTAGE)
