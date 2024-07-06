#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the apply points page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page


def switch_to_ApplyPointsPage(self, user_point_count: int, value_per_point: int, cost_of_test: int):
    points_for_free_test = round(float(cost_of_test) / float(value_per_point))

    user_point_count_float = float(user_point_count)

    enableTenPercentDiscount = points_for_free_test / 10.0 <= user_point_count_float
    self.Discount_10_Percent_Button.setEnabled(enableTenPercentDiscount)

    enable25PercentDiscount = points_for_free_test / 4.0 <= user_point_count_float
    self.Discount_25_Percent_Button.setEnabled(enable25PercentDiscount)

    enable50PercentDiscount = points_for_free_test / 2.0 <= user_point_count_float
    self.Discount_50_Percent_Button.setEnabled(enable50PercentDiscount)

    if user_point_count >= points_for_free_test:
        self.Max_Discount_Button.setText("100% Off")
    else:
        maxPercentDiscount = round(float(user_point_count) / float(points_for_free_test) * 100.0,
                                   2)
        max_points_string = f"{maxPercentDiscount}% Off\n({user_point_count} points)"
        self.Max_Discount_Button.setText(max_points_string)

    self.SetPointsAppliedLabel(float(cost_of_test)/100.0, 0, value_per_point)  # reset apply points page

    """Switch to confirmation page"""
    self._switch_to_page(Page.APPLYPOINTS)


def connect_apply_points_page_buttons(self):
    """Connects the before proceeding page next button"""

    self.Confirm_Apply_Points.clicked.connect(self.Confirm_PointsApplied)
    self.skip_button_apply_points.clicked.connect(self.Skip_PointsApplied)
    self.Discount_10_Percent_Button.clicked.connect(self.Apply10PercentDiscount)
    self.Discount_25_Percent_Button.clicked.connect(self.Apply25PercentDiscount)
    self.Discount_50_Percent_Button.clicked.connect(self.Apply50PercentDiscount)
    self.Max_Discount_Button.clicked.connect(self.ApplyMaxDiscount)


def Confirm_PointsApplied(self):
    self.switch_to_payment_page()


def Skip_PointsApplied(self):
    self.switch_to_payment_page()


def Apply10PercentDiscount(self):
    pass


def Apply25PercentDiscount(self):
    pass


def Apply50PercentDiscount(self):
    pass


def ApplyMaxDiscount(self):
    pass


def SetPointsAppliedLabel(self, cost_of_test_dollars: float, points_applied: int, value_of_point: int):
    cost_of_test_dollars_string = f"{cost_of_test_dollars:.2f}"  # ensure we round to 2 decimals

    self.Points_Being_Applied_lbl.setText(f'Points applied<br><span style="color: #0289c7";>{points_applied}</span>')
    discount_dollars = round(float(points_applied) * float(value_of_point) / 100.0, 2)
    final_cost_dollars = cost_of_test_dollars - discount_dollars
    final_cost_dollars_string = f"{final_cost_dollars:.2f}"  # ensure we round to 2 decimals

    final_cost_cents = max(int(round(final_cost_dollars*100.0)), 0)# force int and 0 as minimum value
    test_cost_string = 'Cost Of Test <br>'
    if points_applied > 0:
        test_cost_string += f'<span style="color: red; text-decoration: line-through;">${cost_of_test_dollars_string}</span><br>'
        if final_cost_cents == 0:
            test_cost_string += "FREE"
        else:
            test_cost_string += f'${final_cost_dollars_string}'

    else:
        test_cost_string += f'<span style="color: white;">{final_cost_dollars_string}</span>\n'

    self.Price_Adjustment_lbl.setText(test_cost_string)
