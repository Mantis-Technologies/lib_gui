#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the results page"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness", "Nick Lanotte", "Michael Mahoney"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from ..page import Page
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QFont, QColor, QBrush, QPixmap, QPainter
from PyQt5.QtCore import Qt


def switch_to_results_page(self):
    """Switches to the results page"""
    self.start_timer_to_ignore_button_presses("Results confirm")
    self._switch_to_page(Page.RESULTS)


def CreatePieSeries(self, analytes):
    newSeries = QPieSeries()
    totalPercentage = 0.0
    for analyte in analytes:
        if "total" in analyte.name.lower():
            continue
        analytePercent = round(analyte.analyte_concentration, 1) / 100.0
        totalPercentage = totalPercentage + analytePercent
        slice_ = QPieSlice(analyte.name, analytePercent)
        slice_.setColor(QColor(analyte.chartColor[0], analyte.chartColor[1], analyte.chartColor[2]))
        slice_.setLabelVisible()
        newSeries.append(slice_)

    if totalPercentage < 1.0:
        slice_ = QPieSlice("NOT TESTED", 1.0 - totalPercentage)
        slice_.setColor(QColor(200, 200, 200))  # light gray
        slice_.setLabelVisible()
        newSeries.append(slice_)
    return newSeries


def set_results_labels(self, analytes):
    newSeries = self.CreatePieSeries(analytes)
    self.UpdateChart(newSeries)
    self.setTotalAnalyteLabels(analytes)


def done_w_results(self):
    """Done with results, move to start page"""
    if self.check_if_button_is_ok_to_press("Results confirm", 2.0):
        self.switch_to_confirm_removal_page()


def connect_results_buttons(self):
    """Connects results buttons"""

    self.finished_test_btn.clicked.connect(self.done_w_results)


def FormatSlices(series, color: str):
    for slice in series.slices():
        font = QFont()
        font.setPointSize(20)  # Change the point size to adjust label size
        font.setFamily("Lato")
        slice.setLabelFont(font)

        if slice.percentage() > 0.25:
            slice.setLabelPosition(QPieSlice.LabelInsideHorizontal)
            # no line break if outside graph
            label = "<p style='color:{}'>{}<br>{}%</p>".format(
                color,
                slice.label(),
                round(slice.percentage() * 100, 1)
            )
            slice.setLabel(label)
        else:
            label = "<p style='color:{}'>{} {}%</p>".format(
                color,
                slice.label(),
                round(slice.percentage() * 100, 1)
            )
            slice.setLabel(label)
        if slice.percentage() > 0.03:
            slice.setLabelVisible()
        else:
            slice.setLabelVisible(False)


def GenerateChartImage(self, imageFileName: str, analytes):
    PDFBackground_color = QColor(255, 255, 255)
    brush = QBrush(PDFBackground_color)

    # Set the background brush for the chart
    self.chart.removeAllSeries()
    self.chart.setBackgroundBrush(brush)
    self.chart_view.setBackgroundBrush(brush)
    newSeries = self.CreatePieSeries(analytes)
    FormatSlices(newSeries, 'black')
    self.chart.addSeries(newSeries)
    self.chart_view.grab().save(imageFileName)


def UpdateChart(self, series):
    self.chart.removeAllSeries()
    FormatSlices(series, 'white')
    self.chart.addSeries(series)
    background_color = QColor(27, 27, 27)
    brush = QBrush(background_color)
    # Set the background brush for the chart
    self.chart.setBackgroundBrush(brush)
    self.chart_view.setBackgroundBrush(brush)


def setup_pie_chart(self):
    self.chart = QChart()
    series = QPieSeries()
    series.append("NOT TESTED", 100)

    self.chart.setTitle("Test Results")
    self.chart.setBackgroundVisible(True)
    font = QFont()
    font.setPointSize(30)  # Change the point size to adjust the font size
    font.setFamily("Monserrat Light")
    self.chart.setTitleFont(font)
    self.chart.setTitleBrush(QColor(255, 255, 255))
    # self.chart.legend().setVisible(False)
    legend = self.chart.legend()

    # Set the alignment of the legend
    legend.setAlignment(Qt.AlignRight)
    legend.setColor(QColor(255, 255, 255))

    results_page_widget = self.stackedWidget.widget(Page.RESULTS.value)
    self.chart_view = QChartView(self.chart)
    self.chart_view.setParent(results_page_widget)
    self.chart_view.setMinimumSize(800, 600)
    self.chart_view.setGeometry(600, 50, 1100, 700)  # Set position and size using geometry


def setTotalAnalyteLabels(self, analytes):
    thcPercent = 0.0
    cbdPercent = 0.0
    for analyte in analytes:
        lowerCaseName = analyte.name.lower()
        if "total" in lowerCaseName:
            if "thc" in lowerCaseName:
                thcPercent = round(analyte.analyte_concentration, 1)
            elif "cbd" in lowerCaseName:
                cbdPercent = round(analyte.analyte_concentration, 1)

    thcLabel = "<p style='color:{}'>{}: {}%</p>".format(
        'white',
        "TOTAL THC",
        thcPercent)
    cbdLabel = "<p style='color:{}'>{}: {}%</p>".format(
        'white',
        "TOTAL CBD",
        cbdPercent)

    font = QFont()
    font.setPointSize(20)  # Change the point size to adjust the font size
    font.setFamily("Lato")

    self.TotalThcLbl.setText(thcLabel)
    self.TotalThcLbl.setAutoFillBackground(False)
    self.TotalThcLbl.setFont(font)

    self.TotalCbdLbl.setText(cbdLabel)
    self.TotalCbdLbl.setAutoFillBackground(False)
    self.TotalCbdLbl.setFont(font)
