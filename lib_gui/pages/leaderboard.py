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
import os
from datetime import datetime, timedelta

# Get the current date
current_date = datetime.now()

# Get the first day of the current month
first_day_of_month = current_date.replace(day=1)

# Calculate the last day of the current month
next_month = first_day_of_month.replace(day=28) + timedelta(days=4)  # this will never fail
last_day_of_month = next_month - timedelta(days=next_month.day)

# Format the dates
first_day_str = first_day_of_month.strftime('%m/%d/%y')
last_day_str = last_day_of_month.strftime('%m/%d/%y')

def switch_to_leaderboard_page(self):
    """Switches to the FAQ page"""
    self._switch_to_page(Page.LEADERBOARD)
    self.LeaderboardPageTimeoutThread = LeaderboardPageTimeoutThread(self)
    self.LeaderboardPageTimeoutThread.signal.connect(self.LeaderboardPageTimeoutCallback)
    self.LeaderboardPageTimeoutThread.start()
    self.display_leaderboard()

def leaderboard_back_to_start_page(self):
    self.LeaderboardPageTimeoutThread.keepRunning = False
    self.reset_leaderboard_scroll()
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

def reset_leaderboard_scroll(self):
    """Resets the leaderboard scroll position to the top"""
    if hasattr(self, 'table_all_time'):
        self.table_all_time.verticalScrollBar().setValue(0)
    if hasattr(self, 'table_monthly'):
        self.table_monthly.verticalScrollBar().setValue(0)


def setup_leaderboard_page(self):
    """Sets up the geometry and layout for the leaderboard page"""

    # Create a container widget for the leaderboards
    self.leaderboard_container = QWidget(self.ui.LeaderboardPage)
    self.leaderboard_container.setGeometry(155, 200, 1600, 850)  # Set x, y, width, height

    outer_layout = QHBoxLayout(self.leaderboard_container)
    outer_layout.setContentsMargins(10, 10, 10, 10)  # Add margins to ensure the rounded corners are visible

    # All Time Leaderboard
    all_time_layout = QVBoxLayout()

    self.label_title_all_time = QLabel('Top 10 THC-A Testers (All Time)', self)
    self.label_title_all_time.setStyleSheet("""
        QLabel {
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 15px;
        }
    """)
    self.label_title_all_time.setAlignment(Qt.AlignCenter)
    all_time_layout.addWidget(self.label_title_all_time)

    self.table_all_time = QTableWidget(self)
    self.setup_table(self.table_all_time)
    all_time_layout.addWidget(self.table_all_time)

    outer_layout.addLayout(all_time_layout)

    # Monthly Leaderboard
    monthly_layout = QVBoxLayout()

    self.label_title_monthly = QLabel(f'Top 10 THC-A Testers (Monthly: {first_day_str} - {last_day_str})', self)
    self.label_title_monthly.setStyleSheet("""
        QLabel {
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 15px;
        }
    """)
    self.label_title_monthly.setAlignment(Qt.AlignCenter)
    monthly_layout.addWidget(self.label_title_monthly)

    self.table_monthly = QTableWidget(self)
    self.setup_table(self.table_monthly)
    monthly_layout.addWidget(self.table_monthly)

    outer_layout.addLayout(monthly_layout)

    self.ui.LeaderboardPage.setStyleSheet("background-color: #1b1b1b;")

def setup_table(self, table):
    """Sets up the properties of a leaderboard table"""
    table.setRowCount(10)  # Assuming top 10 entries
    table.setColumnCount(3)  # Three columns: Rank, User, and THC-A Value
    table.setHorizontalHeaderLabels(['Rank', 'User', 'THC-A Value'])

    table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
    table.horizontalHeader().setDefaultSectionSize(251)  # Adjust column width
    table.verticalHeader().setDefaultSectionSize(75)  # Adjust row height
    table.verticalHeader().setVisible(False)  # Hide vertical header

    table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)  # Disable resizing of columns
    table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)  # Disable resizing of rows
    table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)  # Disable selection
    table.setFocusPolicy(Qt.NoFocus)  # Disable focus

    total_table_height = (table.verticalHeader().defaultSectionSize() * table.rowCount() +
                          table.horizontalHeader().height() +
                          table.frameWidth() * 2)
    table.setFixedHeight(total_table_height)  # Set the fixed height for the table
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove horizontal scrollbar
    table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove vertical scrollbar
    table.setStyleSheet("""
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
            font-size: 22px;
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


def display_leaderboard(self):
    kiosk_id = self.config.KioskID  # Retrieve the kiosk_id from the config

    try:
        # Fetch all-time leaderboard data
        leaderboard_data_all_time = self.get_all_time_leaderboard_data(kiosk_id)
        self.populate_table(self.table_all_time, leaderboard_data_all_time)

        # Fetch monthly leaderboard data
        leaderboard_data_monthly = self.get_monthly_leaderboard_data(kiosk_id)
        self.populate_table(self.table_monthly, leaderboard_data_monthly)

    except Exception as e:
        print(f"Failed to retrieve leaderboard data: {e}")
        # Handle the error (e.g., display an error message on the UI)

def get_all_time_leaderboard_data(self, kiosk_id):
    # This method will be overridden in lib_kiosk
    pass


def get_monthly_leaderboard_data(self, kiosk_id):
    # This method will be overridden in lib_kiosk
    pass

def get_relative_path(relative_path):
    # Adjust the base path to point to the lib_gui directory
    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    full_path = os.path.normpath(os.path.join(base_path, relative_path))
    return full_path

def populate_table(self, table, leaderboard_data):
    """Populates a leaderboard table with data"""
    table.setRowCount(len(leaderboard_data))  # Adjust row count based on data

    for idx, item in enumerate(leaderboard_data):
        # Create rank item with medal images for top 3 spots
        rank_label = QLabel()
        rank_label.setAlignment(Qt.AlignCenter)
        rank_label.setStyleSheet("background-color: #2e2e2e;")  # Set background color

        if idx == 0:
            rank_label.setPixmap(QPixmap(get_relative_path("rank_medal_images/first_place_medal.png")).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif idx == 1:
            rank_label.setPixmap(QPixmap(get_relative_path("rank_medal_images/second_place_medal.png")).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif idx == 2:
            rank_label.setPixmap(QPixmap(get_relative_path("rank_medal_images/third_place_medal.png")).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

        table.setCellWidget(idx, 0, rank_label)
        table.setItem(idx, 1, user_item)
        table.setItem(idx, 2, thca_item)

