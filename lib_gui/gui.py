#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a GUI class"""

__author__ = "Justin Furuness, Nicholas Lanotte, Michael Mahoney"
__credits__ = ["Justin Furuness", "Nicholas Lanotte", "Michael Mahoney"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"


import os
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from .page import Page


class GUI(QtWidgets.QMainWindow):

    gui_ui_fname = "gui.ui"

    def __init__(self, debug=False, fake_backend: bool = False, fake_payment_terminal: bool = False):
        """Connects all buttons and switches to boot page"""

        # Pytest cannot run if this is enabled
        if "PYTEST_CURRENT_TEST" not in os.environ:
            self.app = QApplication(sys.argv)
        super(GUI, self).__init__()

        # If in debug mode, typing n moves to next screen
        self.debug = debug
        self.fake_backend = fake_backend
        self.fake_payment_terminal = fake_payment_terminal
        self.keepThreadsRunning = True

        # Load the UI
        self.ui = uic.loadUi(self.ui_path, self)
        # Connect start buttons
        self.connect_start_buttons()
        # Connect confirmation buttons
        self.connect_confirmation_buttons()
        # Connect loading sample buttons
        self.connect_load_buttons()
        # Connect results buttons
        self.connect_results_buttons()
        # Connect Order Buttons
        self.connect_order_buttons()
        # Connect payment buttons
        self.connect_payment_buttons()
        # Connect instruction page buttons
        self.connect_instruction_buttons()
        # Connect about page buttons
        self.connect_about_buttons()
        # Connect disclaimer page buttons
        self.connect_disclaimer_buttons()
        # Connect before proceeding page buttons
        self.connect_before_proceeding_buttons()
        # Connect rescan results page
        self.connect_rescan_buttons()
        # Connect confirm removal page
        self.connect_confirm_removal_buttons()
        # Connect maintenance page buttons
        self.connect_maintenance_buttons()
        # Set up pie chart
        self.setup_pie_chart()
        # Remove pointless info
        self.setWindowFlag(Qt.FramelessWindowHint)
        # This is only for when in use by a lab
        self.set_visibility_of_lab_items(visible=False)
        # Connect keyboard shortcuts
        self.connect_shortcuts()
        if not self.fake_payment_terminal and not self.fake_backend:
            self.showFullScreen()
        # Move to booting page
        self.switch_to_boot_page()
    def _switch_to_page(self, page: Page):
        """Switches to a page"""

        if not self.debug:
            # Remove cursor unless debugging
            self.setCursor(Qt.BlankCursor)
        # Move to the next page
        self.stackedWidget.setCurrentIndex(page.value)
        # Update and show the new screen
        self.update()
        self.show()

        # Don't bother with this in pytest since we use pytest-qt
        if "PYTEST_CURRENT_TEST" not in os.environ:
            # If you don't do this it waits until func's done w callbacK
            # https://stackoverflow.com/a/2066916/8903959
            self.app.processEvents()
        else:
            # Testing
            assert self.current_page == page

    @property
    def current_page(self):
        """Returns the current page based on the stackwidget index"""

        return Page(self.stackedWidget.currentIndex())

    def close(self):
        """Closes the GUI. Done here for easy inheritance"""

        super(GUI, self).close()
        self.keepThreadsRunning = False

    def ShutdownKiosk(self):
        self.close()
        print("Shutting down")
        import os
        os.system('systemctl poweroff')

        # Boot page methods
    from .pages.boot_page import switch_to_boot_page

    # Start page methods
    from .pages.start_page import switch_to_start_page
    from .pages.start_page import connect_start_buttons

    # Confirmation over 21 page methods
    from .pages.confirmation_page import switch_to_confirmation_page
    from .pages.confirmation_page import connect_confirmation_buttons

    # Order page methods
    from .pages.order_page import switch_to_order_page
    from .pages.order_page import connect_order_buttons
    from .pages.order_page import connect_num_buttons
    from .pages.order_page import connect_del_btn
    from .pages.order_page import get_order_num
    from .pages.order_page import set_order_num
    from .pages.order_page import change_order_id_lbl
    from .pages.order_page import set_visibility_of_lab_items
    from .pages.order_page import get_prep
    from .pages.order_page import get_notes

    # Loading page methods (for loading sample)
    from .pages.load_page import switch_to_load_page
    from .pages.load_page import connect_load_buttons
    from .pages.load_page import cancel_load
    from .pages.load_page import finished_load

    # Scanning page methods (while sample is being scanned)
    from .pages.scanning_page import switch_to_scanning_page

    # Results page methods
    from .pages.results_page import switch_to_results_page
    from .pages.results_page import set_results_labels
    from .pages.results_page import connect_results_buttons
    from .pages.results_page import done_w_results
    from .pages.results_page import setup_pie_chart
    from .pages.results_page import UpdateChart
    from .pages.results_page import CreatePieSeries
    from .pages.results_page import setTotalAnalyteLabels, GenerateChartImage

    #Configuring Keypad page
    from .pages.ConfiguringKeyPadPage import switch_to_ConfiguringKeyPad_page

    # Error page
    from .pages.error_page import switch_to_error_page

    #Payment page
    from .pages.Payment_page import switch_to_payment_page
    from .pages.Payment_page import set_Price_label
    from .pages.Payment_page import connect_payment_buttons
    from .pages.Payment_page import cancel_payment
    from .pages.Payment_page import PaymentApprovedCallback
    from .pages.Payment_page import PaymentTimeoutCallback

    from .pages.instructions_page import (switch_to_instruction_page, connect_instruction_buttons,
                                          next_button_instruction, cancel_button_instruction)
    # About page
    from .pages.About_page import switch_to_about_page, connect_about_buttons, AboutPageTimeoutCallback, BackToStartPageButton

    # Disclaimer page
    from .pages.disclaimer_page import switch_to_disclaimer_page, connect_disclaimer_buttons
    # Before proceeding page
    from .pages.before_proceeding_page import switch_to_before_proceeding_page, connect_before_proceeding_buttons
    # Rescan results page
    from .pages.rescan_results_page import switch_to_rescan_page, connect_rescan_buttons
    # Confirm removal page
    from .pages.confirm_removal_page import switch_to_confirm_removal_page, connect_confirm_removal_buttons

    from .pages.MaintenancePage import switch_to_maintenance_page, connect_maintenance_buttons, MoveToEject, HomeMotionSystem


    # Keyboard shortcut methods
    from .actions import connect_shortcuts
    from .actions import _move_to_next_screen

    def run(self):
        """Runs the app"""
        sys.exit(self.app.exec_())

    @property
    def ui_path(self):
        """Path to the UI file"""

        _dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(_dir, self.gui_ui_fname)

