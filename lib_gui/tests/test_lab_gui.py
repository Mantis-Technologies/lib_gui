#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains tests for the LabGUI class

For specifics on each test, see the docstrings under each function.
"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

import pytest

from lib_enums import Prep

from .test_gui import TestGUI

from ..lab_gui import LabGUI
from ..page import Page


# Overrides the gui fixture for the lab_gui fixture
@pytest.fixture(scope="function")
def gui(qtbot):
    gui = LabGUI()
    qtbot.addWidget(gui)
    return gui


@pytest.mark.lab
class TestLabGUI(TestGUI):
    """Tests all funcs within the LabGUI class"""

    def test_prep_combo_box(self, gui, qtbot):
        """Tests that the GUI combo box methods work"""

        for i in range(gui.prep_combo_box.count()):
            gui.prep_combo_box.setCurrentIndex(i)
            # If any of these were not correct, this method would explode
            assert isinstance(gui.get_prep(), Prep)

    def test_get_notes(self, gui, qtbot):
        """Tests that the GUI combo box methods work"""

        assert gui.get_notes() == ""
        notes = "notes"
        gui.notes_entry.setText(notes)
        assert gui.get_notes() == notes
        gui.switch_to_order_page()
        assert gui.get_notes() == ""

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
        """Not used in lab gui"""

        pass

    def test_gui_confirmation_yes(self, *args):
        """Not used in lab gui"""

        pass

    def test_results_w_analytes(self, gui):
        """Not used in lab gui"""

        pass

    def test_finished_test_btn(self, gui, qtbot):
        """Not used in lab gui"""

        pass
