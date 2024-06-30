from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint


class User_Banner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 100)  # Set a fixed size for the banner

        self.username_lbl = QLabel("Welcome <username>", self)
        self.username_lbl.setGeometry(20, 0, 300, 100)  # Position the label
        self.username_lbl.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0); color: white; font-size: 20px;")  # Style the label
        self.username_lbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Set text alignment to center

        self.user_points_lbl = QLabel("X Points", self)
        self.user_points_lbl.setGeometry(320, 0, 280, 100)  # Position the label
        self.user_points_lbl.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0); color: white; font-size: 40px;")  # Style the label
        self.user_points_lbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Set text alignment to center

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.white, 4)  # Set the pen color and width
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing

        # Set brush to fill the polygon
        brush = QBrush(QColor(3, 116, 64))  # Choose a color for the fill
        painter.setBrush(brush)

        # Get widget dimensions
        width = self.width()
        height = self.height()

        # Define points for the custom shape
        points = [
            QPoint(0, 0),
            QPoint(20, height),
            QPoint(width, height),  # Bottom-right corner
            QPoint(width, 0),  # Top-right corner
            QPoint(0, 0)  # Top-left corner
        ]

        # Draw the custom shape
        painter.drawPolygon(*points)

    def Set_Banner_Info(self, username: str, points: int, is_guest: bool):
        username_string = username
        if is_guest:
            username_string = "Guest"

        username_full_string = f'<p><span style = "font-size:20px;">Welcome</span ><br><span style = ' \
                               f'"font-size:40px;" >{username_string}</span> </p>'
        self.username_lbl.setText(username_full_string)
        points_string = f'{points} Points'
        if is_guest:
            points_string = ""
        self.user_points_lbl.setText(points_string)
