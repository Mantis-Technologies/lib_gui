#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the Lab GUI for testing at labs"""

__author__ = "Justin Furuness, Michael Mahoney"
__credits__ = ["Justin Furuness", "Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

from .gui import GUI
from overrides import override

class LabGUI(GUI):
    """This class is meant for labs and removes several GUI pages"""

    def __init__(self, debug=False, fake_backend: bool = False, *args, **kwargs):
        """Inits gui and modifies for Lab"""
        super(LabGUI, self).__init__(debug=debug, fake_backend=fake_backend, *args, **kwargs)



    @override
    def switch_to_confirmation_page(self):
        """We don't need confirmation page, move straight to order page"""
        print("Switching to Order page")
        self.switch_to_order_page()
        print("Succesfully switched to to Order page")

    @override
    def switch_to_results_page(self):
        """We don't care about results, move straight to order page"""

        self.switch_to_order_page()

    @override
    def switch_to_payment_page(self):
        "We don't care about payment :'( move straight to order page"
        self.switch_to_order_page()
