#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the results page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page


def switch_to_results_page(self):
    """Switches to the results page"""

    self._switch_to_page(Page.RESULTS)


def set_results_labels(self, analytes):
    """Sets labels of results based on analytes"""

    for lbl in [self.results_1_lbl, self.results_2_lbl, self.results_3_lbl,
                self.results_4_lbl, self.results_5_lbl, self.results_6_lbl]:
        lbl.setText("")


    # For mint tea
    # concentration = analytes[0].analyte_concentration * 100
    # concentration = analytes[0].analyte_concentration * 100
    # if concentration <= -11:
    #     results = "Aveda Tea"
    # else:
    #     results = "Mint Tea"
    # results = ""

    # self.results_1_lbl.setText(results)
    elf.results_1_lbl.setText(str(analytes[0]))
    self.results_1_lbl.setStyleSheet("color:black")


def done_w_results(self):
    """Done with results, move to start page"""

    self.switch_to_start_page()


def connect_results_buttons(self):
    """Connects results buttons"""

    self.finished_test_btn.clicked.connect(self.done_w_results)
