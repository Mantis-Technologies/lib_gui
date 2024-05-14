from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
import requests


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

    response = requests.get('https://www.cannacheckkiosk.com/top-thca-testers')
    leaderboard_data = response.json()

    for idx, item in enumerate(leaderboard_data):
        self.table.setItem(idx, 0, QTableWidgetItem(str(item['user_id'])))
        self.table.setItem(idx, 1, QTableWidgetItem(f"{item['max_thca']:.2f}%"))