#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains methods pertaining to the leaderboard page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QWidget, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QColor, QFont, QPalette, QIcon, QPixmap, QImage
import time
import requests


def switch_to_leaderboard_page(self):
    """Switches to the FAQ page"""
    self._switch_to_page(Page.LEADERBOARD)
    self.LeaderboardPageTimeoutThread = LeaderboardPageTimeoutThread(self)
    self.LeaderboardPageTimeoutThread.signal.connect(self.LeaderboardPageTimeoutCallback)
    self.LeaderboardPageTimeoutThread.start()
    self.display_leaderboard()

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


def setup_leaderboard_page(self):
    """Sets up the geometry and layout for the leaderboard page"""

    # Create a container widget for the leaderboard
    self.leaderboard_container = QWidget(self.ui.LeaderboardPage)
    self.leaderboard_container.setGeometry(550, 200, 800, 850)  # Set x, y, width, height

    layout = QVBoxLayout(self.leaderboard_container)

    self.label_title = QLabel('Top 10 THC-A Testers', self)
    self.label_title.setStyleSheet("""
        QLabel {
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 15px;
        }
    """)
    self.label_title.setAlignment(Qt.AlignCenter)
    layout.addWidget(self.label_title)

    # Table to display leaderboard data
    self.table = QTableWidget(self)
    self.table.setRowCount(10)  # Assuming top 10 entries
    self.table.setColumnCount(3)  # Three columns: Rank, User, and THC-A Value
    self.table.setHorizontalHeaderLabels(['Rank', 'User', 'THC-A Value'])
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
    self.table.horizontalHeader().setDefaultSectionSize(247)  # Adjust column width
    self.table.verticalHeader().setDefaultSectionSize(75)  # Adjust row height
    self.table.verticalHeader().setVisible(False)  # Hide vertical header
    total_table_height = (self.table.verticalHeader().defaultSectionSize() * self.table.rowCount() +
                          self.table.horizontalHeader().height() +
                          self.table.frameWidth() * 2)
    self.table.setFixedHeight(total_table_height)  # Set the fixed height for the table
    self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove horizontal scrollbar
    self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove vertical scrollbar
    self.table.setStyleSheet("""
        QTableWidget {
            background-color: #2e2e2e;
            color: white;
            font-size: 18px;
            gridline-color: #444;
            padding: 15px;
            border: 1px solid #444;
            border-radius: 10px;
        }
        QHeaderView::section {
            background-color: #444;
            color: white;
            font-size: 18px;
            padding: 15px;
            border: 1px solid #444;
        }
        QTableWidget QTableCornerButton::section {
            background-color: #444;
            border: 1px solid #444;
        }
        QTableWidget::item {
            border: 1px solid #444;
        }
    """)

    layout.addWidget(self.table)

    self.ui.LeaderboardPage.setStyleSheet("background-color: #1b1b1b;")



def display_leaderboard(self):
    kiosk_id = self.config.KioskID  # Retrieve the kiosk_id from the config

    try:
        response = requests.get(f'http://127.0.0.1:5000/top-thca-testers?kiosk_id={kiosk_id}', headers={"Accept": "application/json"})
        response.raise_for_status()  # Raise an exception for HTTP errors
        leaderboard_data = response.json()

        self.table.setRowCount(len(leaderboard_data))  # Adjust row count based on data
        self.table.setColumnCount(3)  # Three columns: Rank, User, and THC-A Value
        self.table.setHorizontalHeaderLabels(['Rank', 'User', 'THC-A Value'])

        for idx, item in enumerate(leaderboard_data):
            # Create rank item with medal images for top 3 spots
            rank_label = QLabel()
            rank_label.setAlignment(Qt.AlignCenter)
            rank_label.setStyleSheet("background-color: #2e2e2e;")  # Set background color

            if idx == 0:
                rank_label.setPixmap(QPixmap("/Users/tiki/Desktop/Monolith_Kiosk_Code/lib_gui/lib_gui/rank_medal_images/first_place_medal.png").scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            elif idx == 1:
                rank_label.setPixmap(QPixmap("/Users/tiki/Desktop/Monolith_Kiosk_Code/lib_gui/lib_gui/rank_medal_images/second_place_medal.png").scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            elif idx == 2:
                rank_label.setPixmap(QPixmap("/Users/tiki/Desktop/Monolith_Kiosk_Code/lib_gui/lib_gui/rank_medal_images/third_place_medal.png").scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                rank_label.setText(f"#{idx + 1}")
                rank_label.setAlignment(Qt.AlignCenter)
                rank_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background-color: #2e2e2e;
                        font-size: 20px;
                        font-weight: bold;
                        border: 1px solid #444;
                    }
                """)

            user_display = item['user'] if 'user' in item else f"UserID-{item['user_id']}"
            user_item = QTableWidgetItem(user_display)
            user_item.setTextAlignment(Qt.AlignCenter)
            thca_item = QTableWidgetItem(f"{item['THC-A']:.2f}%")
            thca_item.setTextAlignment(Qt.AlignCenter)

            user_item.setFont(QFont("Arial", 20))  # Increase font size
            thca_item.setFont(QFont("Arial", 20))  # Increase font size

            self.table.setCellWidget(idx, 0, rank_label)
            self.table.setItem(idx, 1, user_item)
            self.table.setItem(idx, 2, thca_item)

    except Exception as e:
        print(f"Failed to retrieve leaderboard data: {e}")
        # Handle the error (e.g., display an error message on the UI)
