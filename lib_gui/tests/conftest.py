#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a fixture for the GUI and Lab classes"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

import pytest

from ..gui import GUI


@pytest.fixture(scope="function")
def gui(qtbot):
    gui = GUI()
    qtbot.addWidget(gui)
    return gui
