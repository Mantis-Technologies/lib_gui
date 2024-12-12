#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains methods for the order page"""

__author__ = "Justin Furuness, Michael Mahoney"
__credits__ = ["Justin Furuness", "Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page
from lib_enums import Prep
from PyQt5.QtWidgets import QMessageBox
import os


current_dir = os.path.dirname(os.path.realpath(__file__)) # this returns pages directory
print(current_dir)
parent_dir = os.path.dirname(current_dir)
print(parent_dir)
SAMPLE_FILE = os.path.join(parent_dir, "previous_samples.txt")
print(SAMPLE_FILE)

def commence_lab_app_scan(self):
    """commences scan, overwritten function. loading of sample complete, switch to scanning page"""
    print("Commencing lab app scan")


def switch_to_order_page(self):
    """Switches to order page and clears prev order"""

    self.order_num_entry.clear()
    self.notes_entry.clear()
    self._switch_to_page(Page.ORDER)

    # Display last used sample number if any
    last_sample = get_last_sample_from_file()
    if last_sample is not None:
        self.previous_sample_lbl.setText(f"Previous sample number: {last_sample}")
    else:
        self.previous_sample_lbl.setText("Previous sample number: None")
    self.previous_sample_lbl.show()


def connect_order_buttons(self):
    """Connects order buttons.

    On Next:
    - If order_num exists and is in file, show warning dialog with Cancel and Continue.
      Cancel = stop, Continue = proceed with commence_lab_app_scan().
    - If order_num exists and not in file, add it to file and proceed.
    """

    self.connect_num_buttons()
    self.connect_del_btn()

    def next_page():
        try:
            order_num = self.get_order_num().strip()
            print("Debug: order_num =", order_num)
            if order_num:
                print("Debug: Checking file for sample:", order_num)
                if sample_exists_in_file(order_num):
                    print("Debug: sample found in file")
                    # Show warning dialog
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("This sample number was already used!\nDo you want to continue or cancel?")
                    msg.setWindowTitle("Warning")
                    msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
                    msg.button(QMessageBox.Yes).setText("Continue")
                    response = msg.exec_()

                    if response == QMessageBox.Cancel:
                        # User chose to stop
                        print("Debug: User canceled, not proceeding with scan")
                        return
                    # User chose Continue
                    print("Debug: User chose to continue")
                    self.commence_lab_app_scan()
                else:
                    print("Debug: sample not found in file")
                    # Not in file, add it and commence scan
                    append_sample_to_file(order_num)
                    self.commence_lab_app_scan()
            else:
                print("Debug: No order number entered, do nothing")
        except Exception as e:
            print("Next page failed with ", str(e))

    self.order_num_next_btn.clicked.connect(next_page)
    self.order_num_cancel_btn.clicked.connect(self.switch_to_order_page)


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
        return Prep.MECHANICAL_GRIND
    elif "ground by hand" in text.lower():
        return Prep.HAND_GRIND
    elif "flower intact" in text.lower():
        return Prep.INTACT
    else:
        raise NotImplementedError


def get_notes(self):
    """Returns the notes that were input"""

    return self.notes_entry.toPlainText()

#############################
### File Handling Helpers ###
#############################

def sample_exists_in_file(sample_number: str) -> bool:
    """Check if a sample_number exists in previous_samples.txt"""
    print("Debug: Checking if sample exists in file:", sample_number)
    if not os.path.exists(SAMPLE_FILE):
        print("Debug: File does not exist")
        return False
    with open(SAMPLE_FILE, "r") as f:
        lines = f.read().splitlines()
    print("Debug: file lines =", lines)
    return sample_number in lines

def append_sample_to_file(sample_number: str):
    """Append a new sample_number to the file"""
    with open(SAMPLE_FILE, "a") as f:
        f.write(sample_number + "\n")
    print(f"Debug: Appended {sample_number} to {SAMPLE_FILE}")

def get_last_sample_from_file() -> str:
    """Get the last sample number from the file, or None if empty/no file"""
    if not os.path.exists(SAMPLE_FILE):
        return None
    with open(SAMPLE_FILE, "r") as f:
        lines = f.read().splitlines()
    if lines:
        return lines[-1]
    return None
