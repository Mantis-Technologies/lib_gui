#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a GUI class"""

__author__ = "Justin Furuness, Nicholas Lanotte, Michael Mahoney"
__credits__ = ["Justin Furuness", "Nicholas Lanotte", "Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"


import os
import sys

from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Signal, Qt, QEvent
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QLineEdit
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import QFile
from PySide6.QtCore import QCoreApplication

from .page import Page
import time


class GUI(QtWidgets.QMainWindow):

    def __init__(self, debug=False, fake_backend: bool = False, fake_payment_terminal: bool = False):
        """Connects all buttons and switches to boot page"""
        self.loader = QUiLoader()
        # Pytest cannot run if this is enabled
        if "PYTEST_CURRENT_TEST" not in os.environ:
            self.app = QApplication(sys.argv)
        super(GUI, self).__init__()
        self.load_custom_fonts()
        # If in debug mode, typing n moves to next screen
        self.debug = debug
        self.fake_backend = fake_backend
        self.fake_payment_terminal = fake_payment_terminal
        self.keepThreadsRunning = True
        self.button_delay_map = {} # stores key value pairs for button names and a time. Used to have button presses be ignored for set periods

    def recursiveAddChildrenWidgets(self, parentWidget):
        for widget in parentWidget.children():
            setattr(self, widget.objectName(), widget)
            self.recursiveAddChildrenWidgets(widget)

    def load_ui(self, ui_filename):
        """Loads the appropriate UI based on the kiosk version."""
        print(f"Loading ui {ui_filename}")
        # Save ui filename to a variable to be accessed elsewhere
        ui_version = ui_filename

        # Get the path to the current directory where this script is located
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path to the .ui file based on the current directory
        ui_path = os.path.join(current_dir, ui_filename)

        ##############################################################################
        #The conversion to Pyside 6 has some differences from PyQt5 causing the main
        # window to not be loaded directly. We need to load the ui, promote the widgets
        # within and then resize the main window we made.
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        self.ui = self.loader.load(ui_file, self)
        uiCentralWidget = self.ui.findChild(QWidget, "centralwidget")
        self.recursiveAddChildrenWidgets(uiCentralWidget)
        self.setCentralWidget(uiCentralWidget)
        ui_file.close()
        stackedWidgetSize = self.stackedWidget.size()
        # make all widgets members of self for compatibility with pyqt5 code
        self.resize(stackedWidgetSize.width(), stackedWidgetSize.height())
        ###############################################################################

        # Connect buttons after the UI is loaded
        self.setup_connections(ui_version)

        # Install event filter for finduseradduser page to detect global clicks
        QApplication.instance().installEventFilter(self)

    def setup_connections(self, ui_version):
        """Connects buttons and other widgets to their respective functions. Pass ui version to pages that need it"""
        # Connect start buttons
        print("Initializing: Connecting start buttons")
        self.connect_start_buttons()

        # Connect confirmation buttons
        print("Initializing: Connecting confirmation buttons")
        self.connect_confirmation_buttons()

        # Connect loading sample buttons
        print("Initializing: Connecting loading sample buttons")
        self.connect_load_buttons()

        # Connect results buttons
        print("Initializing: Connecting results buttons")
        self.connect_results_buttons()

        # Connect Order Buttons
        print("Initializing: Connecting order buttons")
        self.connect_order_buttons()

        # Connect payment buttons
        print("Initializing: Connecting payment buttons")
        self.connect_payment_buttons()

        # Connect find user add user buttons
        print("Initializing: Connecting find user/add user buttons")
        self.connect_finduseradduser_buttons()

        # Connect find user add user input fields
        print("Initializing: Setting up find user/add user page")
        self.setup_finduser_adduser_page()

        # Connect instruction page buttons
        print("Initializing: Connecting instruction page buttons")
        self.connect_instruction_buttons()

        # Connect about page buttons
        # print("Initializing: Connecting about page buttons (skipped)")  # Commented out

        # Connect disclaimer page buttons
        print("Initializing: Connecting disclaimer page buttons")
        self.connect_disclaimer_buttons()

        # Connect before proceeding page buttons
        print("Initializing: Connecting before proceeding page buttons")
        self.connect_before_proceeding_buttons()

        # Connect rescan results page
        print("Initializing: Connecting rescan results page")
        self.connect_rescan_buttons()

        # Connect confirm removal page
        print("Initializing: Connecting confirm removal page")
        self.connect_confirm_removal_buttons()

        # Connect maintenance page buttons
        print("Initializing: Connecting maintenance page buttons")
        self.connect_maintenance_buttons()

        # Connect FAQ page buttons
        print("Initializing: Connecting FAQ page buttons")
        self.connect_faq_buttons()

        # Set up FAQ page
        self.setup_faq_page(ui_version)
        # Connect Leaderboard page buttons
        print("Initializing: Connecting leaderboard page buttons")
        self.connect_leaderboard_buttons()

        # Setup the Leaderboard
        self.setup_leaderboard_page(ui_version)
        # Set up QR code label
        self.setup_qr_code_label(ui_version)
        # Set up result url widget
        self.setup_results_url(ui_version)
        # Set up pie chart
        self.setup_pie_chart(ui_version)
        # connect apply points page buttons
        self.connect_apply_points_page_buttons()

        self.Load_Pixmaps_Scanning_Page()

        # This is only for when in use by a lab
        print("Initializing: Setting visibility of lab items to False")
        self.set_visibility_of_lab_items(visible=False)

        # Connect keyboard shortcuts
        print("Initializing: Connecting keyboard shortcuts")
        self.connect_shortcuts()

    def show_main_window(self):
        """Shows UI"""
        # Full-screen and other necessary setup
        if not self.fake_payment_terminal and not self.fake_backend:
            print("Initializing: Showing fullscreen")
            self.showFullScreen()
        else:
            print("Showing UI not full screen")
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.show()
        QCoreApplication.processEvents()
        # Move to the booting page
        self.switch_to_boot_page()

    def process_events(self):
        QCoreApplication.processEvents()


    def _switch_to_page(self, page: Page):
        """Switches to a page"""

        print(f"Switching to page: {page}")  # Debug print

        if not self.debug:
            # Remove cursor unless debugging
            self.setCursor(Qt.BlankCursor)
        # Clear text fields if leaving finduseradduser page
        if self.current_page == Page.FINDUSERADDUSER:
            self.clear_text_fields()
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

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and isinstance(obj, QLineEdit):
            obj.mousePressEvent(event)
        else:
            if not hasattr(self, 'keyboard'):
                return super().eventFilter(obj, event)# early out
            """Detects global clicks so user can close out of keyboard by clicking elsewhere"""
            if event.type() == QEvent.MouseButtonPress and self.keyboard.isVisible():
             # print("Mouse button press detected")  # Debug print
                keyboard_rect = self.keyboard.rect()
                globalPosition = event.globalPos()
                keyboard_pos = self.keyboard.mapFromGlobal(globalPosition)
                if not keyboard_rect.contains(keyboard_pos):
                # print("Hiding keyboard")  # Debug print
                    self.keyboard.hide()
        return super().eventFilter(obj, event)

        # Boot page methods
    def update_price_label(self, price_in_dollars_pre_tax: float):

        # Setting the text of the label
        self.ui.start_price_label.setText(f"${price_in_dollars_pre_tax:.2f}")

        # Setting font for label
        font = QFont("Arial", 25)
        self.ui.start_price_label.setFont(font)

    def load_custom_fonts(self):
        """Load custom fonts (Lato and Montserrat)"""
        # Get the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the absolute paths to the font files
        lato_font_path = os.path.join(current_dir, "fonts", "Lato-Regular.ttf")
        montserrat_font_path = os.path.join(current_dir, "fonts", "Montserrat-VariableFont_wght.ttf")
        montserrat_extra_light_path = os.path.join(current_dir, 'fonts', 'Montserrat-ExtraLight.ttf')

        # Add the fonts
        font_db = QFontDatabase()
        lato_font_id = font_db.addApplicationFont(lato_font_path)
        montserrat_font_id = font_db.addApplicationFont(montserrat_font_path)
        extra_light_font_id = font_db.addApplicationFont(montserrat_extra_light_path)

        # Check if the fonts were loaded successfully
        if lato_font_id == -1:
            print("Lato font could not be loaded.")
        if montserrat_font_id == -1:
            print("Montserrat Light font could not be loaded.")
        if extra_light_font_id == -1:
            print("Montserrat Extra Light could not be loaded.")

    # Boot page methods
    from .pages.boot_page import switch_to_boot_page

    # Start page methods
    from .pages.start_page import switch_to_start_page
    from .pages.start_page import connect_start_buttons, OnBeginButtonPressed

    # Confirmation over 21 page methods
    from .pages.confirmation_page import switch_to_confirmation_page
    from .pages.confirmation_page import connect_confirmation_buttons, over_21_confirm

    # Order page methods
    from .pages.order_page import switch_to_order_page, connect_order_buttons, connect_num_buttons, connect_del_btn, initiate_test, Set_last_order_num_lbl
    from .pages.order_page import get_order_num, OnOrderPageShutDown
    from .pages.order_page import set_order_num
    from .pages.order_page import set_visibility_of_lab_items
    from .pages.order_page import get_prep
    from .pages.order_page import get_notes
    from .pages.order_page import commence_lab_app_scan

    # Loading page methods (for loading sample)
    from .pages.load_page import switch_to_load_page
    from .pages.load_page import connect_load_buttons
    from .pages.load_page import cancel_load
    from .pages.load_page import finished_load

    # Scanning page methods (while sample is being scanned)
    from .pages.scanning_page import switch_to_scanning_page, Load_Pixmaps_Scanning_Page

    # Results page methods
    from .pages.results_page import switch_to_results_page
    from .pages.results_page import set_results_labels
    from .pages.results_page import connect_results_buttons
    from .pages.results_page import done_w_results
    from .pages.results_page import setup_pie_chart
    from .pages.results_page import UpdateChart
    from .pages.results_page import CreatePieSeries
    from .pages.results_page import setTotalAnalyteLabels, GenerateChartImage
    from .pages.results_page import setup_qr_code_label, display_qr_code, setup_results_url, results_url_label_text, set_points_earned_label

    # Configuring Keypad page
    from .pages.ConfiguringKeyPadPage import switch_to_ConfiguringKeyPad_page

    # Error page
    from .pages.error_page import switch_to_error_page

    # Payment page
    from .pages.Payment_page import switch_to_payment_page
    from .pages.Payment_page import set_Price_label
    from .pages.Payment_page import connect_payment_buttons, Check_Payment_Terminal_Connection, Send_CheckPayment_Terminal_Connection_Signal
    from .pages.Payment_page import cancel_payment
    from .pages.Payment_page import PaymentApprovedCallback
    from .pages.Payment_page import PaymentTimeoutCallback

    from .pages.NetworkOutagePage import switch_to_Network_Outage_page

    # Instruction page
    from .pages.instructions_page import (switch_to_instruction_page, connect_instruction_buttons,
                                          next_button_instruction, cancel_button_instruction)
    # Find User / Add User Page
    from .pages.finduseradduser import (switch_to_finduseradduser_page, connect_finduseradduser_buttons,
                                        handle_skip_button, handle_existing_user_button, handle_new_user_button,
                                        setup_finduser_adduser_page, hide_keyboard_if_exists, show_keyboard, focus_widget, clear_text_fields,
                                        Get_User_Credentials_From_Existing_User_Input,
                                        Verify_New_User_information, Validate_new_user_input)

    # About page NO LONGER USING THE ABOUT PAGE, REPLACED WITH FAQ
    # from .pages.About_page import (switch_to_about_page, connect_about_buttons, AboutPageTimeoutCallback,
    #                                BackToStartPageButton)

    # Disclaimer page
    from .pages.disclaimer_page import switch_to_disclaimer_page, connect_disclaimer_buttons, disclaimer_confirmed
    # Before proceeding page
    from .pages.before_proceeding_page import switch_to_before_proceeding_page, connect_before_proceeding_buttons, before_proceeding_confirm
    # Rescan results page
    from .pages.rescan_results_page import switch_to_rescan_page, connect_rescan_buttons, on_cancel_test, on_rescan_test, on_see_results
    # Confirm removal page
    from .pages.confirm_removal_page import switch_to_confirm_removal_page, connect_confirm_removal_buttons, confirm_removal
    # Maintenance page
    from .pages.MaintenancePage import (switch_to_maintenance_page, connect_maintenance_buttons, MoveToEject,
                                        HomeMotionSystem)
    # FAQ Page methods
    from .pages.faq_page import (switch_to_faq_page, connect_faq_buttons, faq_back_to_start_page,
                                 FAQPageTimeoutCallback, setup_faq_page, add_faq, toggle_answer, reset_faq_page)

    # Leaderboard Page methods
    from .pages.leaderboard import (switch_to_leaderboard_page, connect_leaderboard_buttons, setup_leaderboard_page,
                                    display_leaderboard, leaderboard_back_to_start_page, LeaderboardPageTimeoutCallback,
                                    reset_leaderboard_scroll, setup_table, populate_table, get_monthly_leaderboard_data,
                                    get_relative_path, get_all_time_leaderboard_data)

    from .pages.ApplyPointsPage import (switch_to_ApplyPointsPage, connect_apply_points_page_buttons,
        Skip_PointsApplied, Confirm_PointsApplied, Apply10PercentDiscount, Apply25PercentDiscount,
        Apply50PercentDiscount, ApplyMaxDiscount, SetPointsAppliedLabel)

    # Keyboard shortcut methods
    from .actions import connect_shortcuts
    from .actions import _move_to_next_screen

    def run(self):
        """Runs the app"""
        self.app.exec_()

