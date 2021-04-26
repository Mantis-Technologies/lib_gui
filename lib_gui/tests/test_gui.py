#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains tests for the GUI class

For specifics on each test, see the docstrings under each function.
"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from PyQt5 import QtCore
import pytest

from ..gui import GUI
from ..page import Page


@pytest.mark.gui
class TestGUI:
    """Tests all funcs within the GUI class"""

    def test_gui_start(self, gui, qtbot):
        """Tests boot, start"""

        assert gui.current_page == Page.BOOTING
        # Calibrated. Move to start.
        gui.switch_to_start_page()
        assert gui.current_page == Page.START
        # Click the start button
        self._click(gui.begin_btn, qtbot)
        assert gui.current_page == Page.CONFIRMATION

    def test_gui_confirmation_no(self, gui, qtbot):
        """Tests that the user is sent back to start if not over 21"""

        # Click not over 21
        self._click(gui.no_not_21_btn, qtbot)
        assert gui.current_page == Page.START

    def test_gui_confirmation_yes(self, gui, qtbot):
        """Tests that the user is sent to order page if over 21"""

        # Click yes over 21
        self._click(gui.yes_over_21_btn, qtbot)
        assert gui.current_page == Page.ORDER

    @pytest.mark.parametrize("order, new_order",
                             [[None, ''], ["123", "12"]]) 
    def test_gui_order_delete(self, gui, qtbot, order, new_order):
        """Tests functionality of the delete button for the order form

        if the form is blank, it should do nothing
        if the form is not blank, it should remove a number

        also tests the get and set order num methods
        """

        if order:
            gui.set_order_num(order)

        self._click(gui.delete_btn, qtbot)

        assert gui.get_order_num() == new_order
        

    def test_gui_order_nums(self, gui, qtbot):
        """Tests all of the order buttons"""

        num_btns = [gui.zero_btn, gui.one_btn, gui.two_btn, gui.three_btn,
                    gui.four_btn, gui.five_btn, gui.six_btn, gui.seven_btn,
                    gui.eight_btn, gui.nine_btn]
    
        total_text = ""
        for i, btn in enumerate(num_btns):
            self._click(btn, qtbot)
            total_text += str(i)
            assert gui.get_order_num() == total_text

    @pytest.mark.parametrize("order", ["", "123"])
    def test_order_num_next_btn(self, gui, qtbot, order):
        """Tests the order num next btn

        If order number is none, do nothing
        """

        gui.switch_to_order_page()
    
        gui.set_order_num(order)

        self._click(gui.order_num_next_btn, qtbot)

        correct_page = Page.LOAD if order else Page.ORDER
        
        assert gui.current_page == correct_page

    def test_order_num_cancel_btn(self, gui, qtbot):
        """Tests the order num cancel btn"""

        gui.switch_to_order_page()

        self._click(gui.order_num_cancel_btn, qtbot)

        assert gui.current_page == Page.START

    def test_results_w_analytes(self, gui):
        """Tests that the results are properly set"""

        test_str = "test"

        gui.set_results_labels([test_str])
        assert gui.results_1_lbl.text() == test_str

    def test_finished_test_btn(self, gui, qtbot):
        """Tests that the finished test btn returns to start"""

        gui.switch_to_results_page()
        self._click(gui.finished_test_btn, qtbot)
        assert gui.current_page == Page.START

    def _click(self, btn, qtbot):
        """Clicks button"""

        qtbot.mouseClick(btn, QtCore.Qt.LeftButton)
