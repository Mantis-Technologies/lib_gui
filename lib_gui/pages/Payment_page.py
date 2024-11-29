#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the payment page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page
from PySide6.QtCore import QThread, Signal, Qt, QObject
from PySide6.QtGui import QFont
import time


def switch_to_payment_page(self):
    """Switches to the results page"""
    self.transactionInProgress = True
    self._switch_to_page(Page.PAYMENT)
    self.CheckPaymentApprovedThread = CheckPaymentApprovedThread(self)
    self.CheckPaymentApprovedThread.signal.connect(self.PaymentApprovedCallback)
    self.CheckPaymentApprovedThread.start()

    self.PaymentTimeoutThread = PaymentTimeoutThread(self)
    self.PaymentTimeoutThread.signal.connect(self.PaymentTimeoutCallback)
    self.PaymentTimeoutThread.start()


def set_Price_label(self, price_in_dollars_total: float):
    # Setting the text of the label
    self.Price_lbl.setText(f"${price_in_dollars_total:.2f}")
    # Setting font for label
    font = QFont("Arial", 50)
    self.Price_lbl.setFont(font)


def cancel_payment(self):
    """User Cancelled payment, move to start page"""
    self.transactionInProgress = False
    self.CheckPaymentApprovedThread.keepRunning = False
    self.PaymentTimeoutThread.keepRunning = False
    self.switch_to_start_page_terminate_transaction()

class CheckPaymentTerminalSignalEmitter(QObject):
    # Define the signal at the class level
    signal = Signal()

    def __init__(self):
        super().__init__()

    def emit_signal(self):
        self.signal.emit()

def connect_payment_buttons(self):
    """Connects results buttons"""

    self.cancel_payment_btn.clicked.connect(self.cancel_payment)

    self.check_payment_terminal_connection_signal = CheckPaymentTerminalSignalEmitter()
    self.check_payment_terminal_connection_signal.signal.connect(self.Check_Payment_Terminal_Connection)


def PaymentApprovedCallback(self, result):
    if self.PaymentTimeoutThread.keepRunning is True:
        self.PaymentTimeoutThread.keepRunning = False
        self.switch_to_instruction_page()


def PaymentTimeoutCallback(self, result):
    self.cancel_payment()


def Check_Payment_Terminal_Connection(self):
    print("Check Payment Terminal function is not overridden")  # override this function


def Send_CheckPayment_Terminal_Connection_Signal(self):
    self.check_payment_terminal_connection_signal.emit_signal()


class PaymentTimeoutThread(QThread):
    signal = Signal('PyQt_PyObject')

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui
        self.keepRunning = True

    def run(self):
        maxSecondsToWait = 100  # the payment terminal times out after 90 seconds. Have this wait slightly more incase the user swipes card at last second
        while self.keepRunning and self.gui.keepThreadsRunning:
            maxSecondsToWait = maxSecondsToWait - 1
            if maxSecondsToWait == 0:
                self.signal.emit(1)  # emit anything to trigger page change
                break
            time.sleep(1)


class CheckPaymentApprovedThread(QThread):
    signal = Signal('PyQt_PyObject')

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui
        self.keepRunning = True

    def run(self):
        while self.keepRunning and self.gui.keepThreadsRunning:
            isApproved, isActiveTransaction = self.gui.paymentTerminal.CheckIfTransactionIsFinished()
            if isApproved and isActiveTransaction:
                self.signal.emit(1)  # emit anything to trigger page change
                break
            time.sleep(0.1)
