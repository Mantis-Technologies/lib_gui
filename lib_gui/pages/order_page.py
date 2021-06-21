#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains methods for the order page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from lib_enums import Prep

from ..page import Page


def switch_to_order_page(self):
    """Switches to order page and clears prev order"""

    self.order_num_entry.clear()
    self._switch_to_page(Page.ORDER)


def connect_order_buttons(self):
    """Connects order buttons

    Won't move to next screen unless there is an order num
    """

    self.connect_num_buttons()
    self.connect_del_btn()

    # If there is no order number, do nothing
    def next_page():
        if len(self.get_order_num()) > 0:
            self.switch_to_load_page()
    self.order_num_next_btn.clicked.connect(next_page)
    self.order_num_cancel_btn.clicked.connect(self.switch_to_start_page)


def connect_num_buttons(self):
    """Connects all number buttons"""

    # Note: for some reason this fails in a loop.
    # No clue why, it appears to be a pyqt5 bug
    # I cannot get it to work even when I processEvents
    # So i have coded it as such

    self.one_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.one_btn.text()))
    self.two_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.two_btn.text()))
    self.three_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.three_btn.text()))
    self.four_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.four_btn.text()))
    self.five_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.five_btn.text()))
    self.six_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.six_btn.text()))
    self.seven_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.seven_btn.text()))
    self.eight_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.eight_btn.text()))
    self.nine_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.nine_btn.text()))
    self.zero_btn.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.zero_btn.text()))


def connect_del_btn(self):
    """Connects delete button"""

    def func():
        """Removes last number"""
        self.set_order_num(self.get_order_num()[:-1])

    self.delete_btn.clicked.connect(func)


def set_visibility_of_prep_combo_box(self, visible=False):
    """Sets and enables preparation methods combo box

    Set visible when in MCR mode since we need that data
    otherwise it defaults to hand grind
    """

    self.prep_combo_box.setVisible(visible)
    self.prep_combo_box.setEnabled(visible)


def get_order_num(self):
    """Returns the order number as a string"""

    return self.order_num_entry.text()


def set_order_num(self, num: str):
    """Sets the order number

    Used when clicking the number buttons
    """

    assert isinstance(num, str)
    return self.order_num_entry.setText(num)


def change_order_id_lbl(self):
    """Changes order id for mcr lab techs"""

    self.enter_id_lbl.setText("Enter sample ID")


def get_prep(self):
    """Gets the preparation method"""

    text = self.prep_combo_box.currentText()
    if "mechanical grind" in text.lower():
        return Prep.MECHANICAL_GRIND
    elif "ground by hand" in text.lower():
        return Prep.HAND_GRIND
    elif "flower intact" in text.lower():
        return Prep.INTACT
    else:
        raise NotImplementedError
