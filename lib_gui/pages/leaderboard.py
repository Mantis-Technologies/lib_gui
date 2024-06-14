#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains methods pertaining to the leaderboard page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import time
import requests


def switch_to_leaderboard_page(self):
    """Switches to the FAQ page"""
    self._switch_to_page(Page.LEADERBOARD)
    self.LeaderboardPageTimeoutThread = LeaderboardPageTimeoutThread(self)
    self.LeaderboardPageTimeoutThread.signal.connect(self.LeaderboardPageTimeoutCallback)
    self.LeaderboardPageTimeoutThread.start()

def leaderboard_back_to_start_page(self):
    self.LeaderboardPageTimeoutThread.keepRunning = False
    self.switch_to_start_page()

def LeaderboardPageTimeoutCallback(self, result):
    self.leaderboard_back_to_start_page()

class LeaderboardPageTimeoutThread(QThread):
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

def connect_leaderboard_buttons(self):
    """Connects Leaderboard buttons"""
    self.leaderboard_back_btn.clicked.connect(self.leaderboard_back_to_start_page)

def set_leaderboard_geometry(self):
    self.setGeometry(100, 100, 800, 600)
    self.setWindowTitle('THC-A Leaderboard')

    self.layout = QVBoxLayout()
    self.label_title = QLabel('Top 10 THC-A Testers', self)
    self.label_title.setStyleSheet("font-size: 24px; font-weight: bold;")
    self.layout.addWidget(self.label_title)

    # Table to display leaderboard data
    self.table = QTableWidget(self)
    self.table.setRowCount(10)  # Assuming top 10 entries
    self.table.setColumnCount(2)  # Two columns: User ID and THC-A Value
    self.table.setHorizontalHeaderLabels(['User ID', 'THC-A Value'])
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only

    # Display dummy leaderboard data
    self.display_leaderboard()

    self.layout.addWidget(self.table)
    self.setLayout(self.layout)


def display_leaderboard(self):
    # Dummy data for testing the display
    # dummy_data = [
    #     {"user_id": 1, "max_thca": 25.5},
    #     {"user_id": 2, "max_thca": 24.3},
    #     {"user_id": 3, "max_thca": 23.8},
    #     {"user_id": 4, "max_thca": 22.9},
    #     {"user_id": 5, "max_thca": 22.1},
    #     {"user_id": 6, "max_thca": 21.5},
    #     {"user_id": 7, "max_thca": 20.9},
    #     {"user_id": 8, "max_thca": 19.8},
    #     {"user_id": 9, "max_thca": 19.3},
    #     {"user_id": 10, "max_thca": 18.7}
    # ]

    response = requests.get('https://www.cannacheckkiosk.com/top-thca-testers') # change so each kiosk has its own leaderboard
    leaderboard_data = response.json()

    for idx, item in enumerate(leaderboard_data):
        self.table.setItem(idx, 0, QTableWidgetItem(str(item['user_id'])))
        self.table.setItem(idx, 1, QTableWidgetItem(f"{item['max_thca']:.2f}%"))