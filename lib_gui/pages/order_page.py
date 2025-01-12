#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains methods for the order page"""

__author__ = "Justin Furuness, Michael Mahoney"
__credits__ = ["Justin Furuness", "Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page
from lib_enums import Prep
from .GetUiDirectoryUtilities import GetCannaCheckUiImagePath
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QObject, Signal


class UpdateLastScanSignalEmitter(QObject):
    # Define the signal at the class level
    signal = Signal(object)

    def __init__(self):
        super().__init__()

    def emit_signal(self, last_scan):
        self.signal.emit(last_scan)


def commence_lab_app_scan(self):
    """commences scan, overwritten function. loading of sample complete, switch to scanning page"""
    print("Commencing lab app scan")


def switch_to_order_page(self):
    """Switches to order page and clears prev order"""

    self.order_num_entry.clear()
    self.notes_entry.clear()
    self._switch_to_page(Page.ORDER)


def Set_last_order_num_lbl(self, label_str: str):
    self.previous_sample_lbl.setText(label_str)
    self.previous_sample_lbl.show()


def initiate_test(self):
    pass


def OnOrderPageShutDown(self):
    pass


def connect_order_buttons(self):
    """Connects order buttons."""

    self.connect_num_buttons()
    self.connect_del_btn()

    logoPath = GetCannaCheckUiImagePath("White logo - no background-greenlogo.png")
    pixmap = QPixmap(logoPath)  # Replace with the path to your image
    # Set the pixmap to the QLabel
    self.cannacheck_logo_label_2.setPixmap(pixmap)

    self.initiate_test_btn.clicked.connect(self.initiate_test)
    self.order_num_cancel_btn.clicked.connect(self.switch_to_order_page)
    self.Lab_ShutDown_Btn.clicked.connect(self.OnOrderPageShutDown)

    self.update_last_scan_signal = UpdateLastScanSignalEmitter()
    self.update_last_scan_signal.signal.connect(self.Update_last_scan_callback)


def Signal_Update_last_scan_and_switch_to_order_page(self, last_scan):
    self.update_last_scan_signal.emit_signal(last_scan)


def Update_last_scan_callback(self, last_scan):
    self.Set_last_order_num_lbl(f"Previous sample number: {last_scan}")
    self.order_num_entry.clear()
    self.notes_entry.clear()
    self._switch_to_page(Page.ORDER)


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


def set_visibility_of_lab_items(self, visible=False):
    """Sets and enables preparation methods combo box

    Set visible when in Lab mode since we need that data
    otherwise it defaults to hand grind
    """

    for box in [self.prep_combo_box,
                self.notes_entry]:
        box.setVisible(visible)
        box.setEnabled(visible)


def get_order_num(self):
    """Returns the order number as a string"""

    return self.order_num_entry.text()


def set_order_num(self, num: str):
    """Sets the order number

    Used when clicking the number buttons
    """

    assert isinstance(num, str)
    return self.order_num_entry.setText(num)


def get_prep(self):
    """Gets the preparation method"""

    text = self.prep_combo_box.currentText()

    if "mcr method - scissors" in text.lower():
        return Prep.HAND_GRIND  # treat scissors as hand grind
    elif "mechanical grind" in text.lower():
        return Prep.MECHANICAL_GRIND
    elif "flower intact" in text.lower():
        return Prep.INTACT
    else:
        raise NotImplementedError


def get_notes(self):
    """Returns the notes that were input"""

    return self.notes_entry.toPlainText()
