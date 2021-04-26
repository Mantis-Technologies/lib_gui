#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a fixture for the GUI and MCR classes"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

import pytest

from ..gui import GUI
from ..mcr_gui import MCRGUI



@pytest.fixture(scope="function")
def gui(qtbot):
    gui = GUI()
    qtbot.addWidget(gui)
    return gui

@pytest.fixture(scope="function")
def mcr_gui(qtbot):
    mcr_gui = MCRGUI()
    qtbot.addWidget(mcr_gui)
    return mcr_gui
