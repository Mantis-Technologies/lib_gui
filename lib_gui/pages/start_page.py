from PyQt5.QtCore import Qt

from ..page import Page

def switch_to_start_page(self):
    self._switch_to_page(Page.START)

def connect_start_buttons(self):
    self.BeginButton.clicked.connect(self.switch_to_confirmation_page)
