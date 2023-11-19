#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the payment page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page
from PyQt5.QtCore import QThread, pyqtSignal, Qt


def switch_to_payment_page(self):
    """Switches to the results page"""
    self.transactionInProgress = True
    self._switch_to_page(Page.PAYMENT)
    self.CheckPaymentApprovedThread = CheckPaymentApprovedThread(self)
    self.CheckPaymentApprovedThread.signal.connect(self.PaymentApprovedCallback)
    self.CheckPaymentApprovedThread.start()


def set_Price_label(self, priceAsInt: int):
    priceAsFloat = float(priceAsInt) / 100.0
    self.Price_lbl.setText(str(priceAsFloat))


def cancel_payment(self):
    """User Cancelled payment, move to start page"""
    self.transactionInProgress = False
    self.CheckPaymentApprovedThread.keepRunning = False
    self.switch_to_start_page_terminate_transaction()


def connect_payment_buttons(self):
    """Connects results buttons"""

    self.cancel_payment_btn.clicked.connect(self.cancel_payment)


def PaymentApprovedCallback(self, result):
    self.switch_to_load_page()


class CheckPaymentApprovedThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui
        self.NextCalibrationTime = 0  # in milliseconds
        self.keepRunning = True

    def run(self):
        while self.keepRunning and self.gui.keepThreadsRunning:
            isApproved, isActiveTransaction = self.gui.paymentTerminal.CheckIfTransactionIsFinished()
            if isApproved and isActiveTransaction:
                self.signal.emit(1)  # emit anything to trigger page change
                break
