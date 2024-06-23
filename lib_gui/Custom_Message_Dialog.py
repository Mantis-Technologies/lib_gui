from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QEvent, QTimer


class CustomMessageBox(QMessageBox):
    def __init__(self, parent=None, *args, **kwargs):
        super(CustomMessageBox, self).__init__(parent, *args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)

        # print("CustomMessageBox created")  # Debug print

        # Set a timer to close the message box after 4 seconds (4000 milliseconds)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.handle_close)
        self.timer.start(4000)
        # print("Timer started for 4 seconds")  # Debug print

        # Ensure the message box appears in front
        self.raise_()
        self.activateWindow()

        # Remove default buttons
        self.setStandardButtons(QMessageBox.NoButton)

    def showEvent(self, event):
        super(CustomMessageBox, self).showEvent(event)
        # print("CustomMessageBox shown")  # Debug print

    def handle_close(self):
        # print("Handling CustomMessageBox close")  # Debug print
        self.accept()  # Close the message box


def ShowCustomMessage(parent, message: str):
    msg_box = CustomMessageBox(parent)
    msg_box.setText(message)
    msg_box.show()
