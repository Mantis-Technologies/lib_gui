from PyQt5.QtCore import Qt

from ..page import Page

def switch_to_confirmation_page(self):
    self._switch_to_page(Page.CONFIRMATION)

def connect_confirmation_buttons(self):
    self.no_not_21_btn.clicked.connect(self.switch_to_start_page)
    self.yes_over_21_btn.clicked.connect(self.switch_to_order_page)
