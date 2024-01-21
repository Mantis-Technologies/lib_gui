#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains all methods relating to the start page"""

__author__ = "Nicholas Lanotte"
__credits__ = ["Nicholas Lanotte"]
__maintainer__ = "Nicholas Lanotte"
__email__ = "nickjl0809@gmail.com"

from ..page import Page
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import time


def switch_to_about_page(self):
    """Switches to the about page"""

    self._switch_to_page(Page.ABOUT)
    self.aboutPageTimeoutThread = AboutPageTimeoutThread(self)
    self.aboutPageTimeoutThread.signal.connect(self.AboutPageTimeoutCallback)
    self.aboutPageTimeoutThread.start()


def BackToStartPageButton(self):
    self.aboutPageTimeoutThread.keepRunning = False
    self.switch_to_start_page()


def AboutPageTimeoutCallback(self, result):
    self.BackToStartPageButton()


def connect_about_buttons(self):
    """Connects the start page begin button"""

    self.back_to_start_btn.clicked.connect(self.BackToStartPageButton)


class AboutPageTimeoutThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui
        self.keepRunning = True

    def run(self):
        maxSecondsToWait = 300  # allow the user 5 minutes to read the page or revert back
        while self.keepRunning and self.gui.keepThreadsRunning:
            maxSecondsToWait = maxSecondsToWait - 1
            if maxSecondsToWait == 0:
                self.signal.emit(1)  # emit anything to trigger page change
                break
            time.sleep(1)
