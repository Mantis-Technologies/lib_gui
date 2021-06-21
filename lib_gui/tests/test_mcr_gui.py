#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains tests for the MCRGUI class

For specifics on each test, see the docstrings under each function.
"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

import pytest

from lib_enums import Prep

from .test_gui import TestGUI

from ..mcr_gui import MCRGUI
from ..page import Page


# Overrides the gui fixture for the mcr_gui fixture
@pytest.fixture(scope="function")
def gui(qtbot):
    gui = MCRGUI()
    qtbot.addWidget(gui)
    return gui


@pytest.mark.mcr
class TestMCRGUI(TestGUI):
    """Tests all funcs within the MCRGUI class"""

    def test_prep_combo_box(self, gui, qtbot):
        """Tests that the GUI combo box methods work"""

        for i in range(gui.prep_combo_box.count()):
            gui.prep_combo_box.setCurrentIndex(i)
            # If any of these were not correct, this method would explode
            assert isinstance(gui.get_prep(), Prep)

###########################
### Overriden functions ###
###########################

    def test_gui_start(self, gui, qtbot):
        """Tests boot, start"""

        assert gui.current_page == Page.BOOTING
        # Calibrated. Move to start.
        gui.switch_to_start_page()
        assert gui.current_page == Page.START
        # Click the start button
        self._click(gui.begin_btn, qtbot)
        assert gui.current_page == Page.ORDER

    def test_gui_confirmation_no(self, *args):
        """Not used in mcr gui"""

        pass

    def test_gui_confirmation_yes(self, *args):
        """Not used in mcr gui"""

        pass

    def test_results_w_analytes(self, gui):
        """Not used in mcr gui"""

        pass

    def test_finished_test_btn(self, gui, qtbot):
        """Not used in mcr gui"""

        pass
