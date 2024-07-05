from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint


class Error_Message_Banner(QWidget):
    def __init__(self, parent=None, ):
        super().__init__(parent)

        self.setFixedSize(1000, 100)  # Set a fixed size for the banner

        self.message_lbl = QLabel("Message_Here", self)
        self.message_lbl.setGeometry(0, 0, 980, 100)  # Position the label
        self.message_lbl.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0); color: white; font-size: 30px;")  # Style the label
        self.message_lbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # Set text alignment to center

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.white, 4)  # Set the pen color and width
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing

        # Set brush to fill the polygon
        brush = QBrush(QColor(169, 6, 10))  # Choose a color for the fill
        painter.setBrush(brush)

        # Get widget dimensions
        width = self.width()
        height = self.height()

        # Define points for the custom shape
        points = [
            QPoint(0, 0),  # top left corner
            QPoint(width, 0),  # Top-right corner
            QPoint(width - 20, height),  # bottom right
            QPoint(0, height),  # bottom Left
            QPoint(0, 0)  # Top-left corner
        ]

        # Draw the custom shape
        painter.drawPolygon(*points)

    def ShowMessage(self, message_to_show: str):
        self.message_lbl.setText(message_to_show)

    def handle_close(self):
        self.hide()
