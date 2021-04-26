#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the MCR GUI for testing at MCR labs"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from .gui import GUI


class MCRGUI(GUI):
    """This class is meant for MCR labs and removes several GUI pages"""

    def __init__(self, *args, **kwargs):
        """Inits gui and modifies for MCR"""

        super(MCRGUI, self).__init__(*args, **kwargs)
        # Changes order label and says it's for sample_id
        self.change_order_id_lbl()
        # Changes the visibility of the preparation method combo box
        self.set_visibility_of_prep_combo_box(visible=True)

    def switch_to_confirmation_page(self):
        """We don't need confirmation page, move straight to order page"""

        self.switch_to_order_page()

    def switch_to_results_page(self):
        """We don't care about results, move straight to order page"""

        self.switch_to_order_page()
