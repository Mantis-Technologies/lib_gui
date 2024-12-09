#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the Lab GUI for testing at labs"""

__author__ = "Justin Furuness, Michael Mahoney"
__credits__ = ["Justin Furuness", "Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

from .gui import GUI


class LabGUI(GUI):
    """This class is meant for labs and removes several GUI pages"""

    def __init__(self, *args, **kwargs):
        """Inits gui and modifies for Lab"""

        # Override unnecessary components
        print("LabGUI: Overriding unnecessary components")
        self.override_unused_components()

        super(LabGUI, self).__init__(*args, **kwargs)
        # Changes order label and says it's for sample_id
        self.change_order_id_lbl()
        # Changes the visibility of the preparation method combo box
        self.set_visibility_of_lab_items(visible=True)


        self.connect_lab_buttons()

    # Override unused methods
    def override_unused_components(self):
        """Skip connecting unused components"""
        self.connect_faq_buttons = lambda: print("Skipping FAQ buttons for LabGUI")
        self.connect_leaderboard_buttons = lambda: print("Skipping leaderboard buttons for LabGUI")
        self.setup_leaderboard_page = lambda: print("Skipping leaderboard setup for LabGUI")
        self.setup_faq_page = lambda: print("Skipping FAQ setup for LabGUI")
        self.connect_apply_points_page_buttons = lambda: print("Skipping apply points page buttons for LabGUI")
        self.setup_qr_code_label = lambda: print("Skipping QR code label setup for LabGUI")
        self.setup_results_url = lambda: print("Skipping results URL setup for LabGUI")
        self.setup_pie_chart = lambda: print("Skipping pie chart setup for LabGUI")

    def connect_maintenance_buttons(self):
        print("Skipping connect maintenance buttons.")

    def connect_lab_buttons(self):
        """Connect only essential buttons for the lab environment"""
        self.connect_order_buttons()
        self.connect_start_buttons()

    def switch_to_confirmation_page(self):
        """We don't need confirmation page, move straight to order page"""
        print("Switching to Order page")
        self.switch_to_order_page()
        print("Succesfully switched to to Order page")

    def switch_to_results_page(self):
        """We don't care about results, move straight to order page"""

        self.switch_to_order_page()

    def switch_to_payment_page(self):
        "We don't care about payment :'( move straight to order page"
        self.switch_to_order_page()
