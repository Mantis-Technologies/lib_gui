#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the apply points page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page


def switch_to_ApplyPointsPage(self, user_name: str, user_point_count: int, value_per_point: int, cost_of_test: int):

    self.Welcome_lbl.setText("Welcome " + user_name)
    self.User_Total_Points_lbl.setText("You have " + str(user_point_count) + " points")

    points_for_free_test = round(float(cost_of_test) / float(value_per_point))

    user_point_count_float = float(user_point_count)

    enableTenPercentDiscount = points_for_free_test/10.0 <= user_point_count_float
    self.Discount_10_Percent_Button.setEnabled(enableTenPercentDiscount)

    enable25PercentDiscount = points_for_free_test/4.0 <= user_point_count_float
    self.Discount_25_Percent_Button.setEnabled(enable25PercentDiscount)

    enable50PercentDiscount = points_for_free_test / 2.0 <= user_point_count_float
    self.Discount_50_Percent_Button.setEnabled(enable50PercentDiscount)

    if user_point_count >= points_for_free_test:
        self.Max_Discount_Button.setText("100% Off")
    else:
        maxPercentDiscount = round(float(user_point_count) / float(points_for_free_test) * 100.0, 2)
        max_points_string = f"{maxPercentDiscount}% Off\n({user_point_count} points)"
        self.Max_Discount_Button.setText(max_points_string)

    """Switch to confirmation page"""
    self._switch_to_page(Page.APPLYPOINTS)


def connect_ApplyPointsPage_buttons(self):
    """Connects the before proceeding page next button"""

    self.Confirm_Apply_Points.clicked.connect(self.Confirm_PointsApplied)
    self.skip_button_apply_points.clicked.connect(self.Skip_PointsApplied)


def Confirm_PointsApplied(self):
    self._switch_to_page(Page.INSTRUCTIONS)


def Skip_PointsApplied(self):
    self._switch_to_page(Page.INSTRUCTIONS)


