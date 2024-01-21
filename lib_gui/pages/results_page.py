#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the results page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QFont, QColor


def switch_to_results_page(self):
    """Switches to the results page"""

    self._switch_to_page(Page.RESULTS)


def CreatePieSeries(self, analytes):
    newSeries = QPieSeries()
    totalPercentage = 0.0
    for analyte in analytes:
        analytePercent = round(analyte.analyte_concentration, 1) / 100.0
        totalPercentage = totalPercentage + analytePercent
        slice_ = QPieSlice(analyte.name, analytePercent)
        slice_.setColor(QColor(analyte.chartColor[0], analyte.chartColor[1], analyte.chartColor[2]))
        slice_.setLabelVisible()
        newSeries.append(slice_)

    if totalPercentage < 1.0:
        slice_ = QPieSlice("Not Tested", 1.0 - totalPercentage)
        slice_.setColor(QColor(200, 200, 200))  # light gray
        slice_.setLabelVisible()
        newSeries.append(slice_)
    return newSeries


def set_results_labels(self, analytes):
    newSeries = self.CreatePieSeries(analytes)
    self.UpdateChart(newSeries)


def done_w_results(self):
    """Done with results, move to start page"""

    self.switch_to_start_page()


def connect_results_buttons(self):
    """Connects results buttons"""

    self.finished_test_btn.clicked.connect(self.done_w_results)


def UpdateChart(self, series):
    self.chart.removeAllSeries()
    for slice in series.slices():
        font = QFont()
        font.setPointSize(20)  # Change the point size to adjust label size
        slice.setLabelFont(font)

        slice.setLabelVisible()
        if slice.percentage() > 0.25:
            slice.setLabelPosition(QPieSlice.LabelInsideHorizontal)
            # no line break if outside graph
            label = "<p style='color:{}'>{}<br>{}%</p>".format(
                'black',
                slice.label(),
                round(slice.percentage() * 100, 1)
            )
            slice.setLabel(label)
        else:
            label = "<p style='color:{}'>{} {}%</p>".format(
                'black',
                slice.label(),
                round(slice.percentage() * 100, 1)
            )
            slice.setLabel(label)
    self.chart.addSeries(series)


def setup_pie_chart(self):
    self.chart = QChart()

    series = QPieSeries()
    series.append("Not Tested", 50)
    series.append("Fake Analyte", 50)

    self.chart.setTitle("Test Results")
    font = QFont()
    font.setPointSize(30)  # Change the point size to adjust the font size
    font.setFamily("Calibri")
    self.chart.setTitleFont(font)
    self.chart.legend().setVisible(False)

    results_page_widget = self.stackedWidget.widget(Page.RESULTS.value)
    self.chart_view = QChartView(self.chart)
    self.chart_view.setParent(results_page_widget)
    self.chart_view.setMinimumSize(800, 600)
    self.chart_view.setGeometry(550, 50, 1200, 980)  # Set position and size using geometry
