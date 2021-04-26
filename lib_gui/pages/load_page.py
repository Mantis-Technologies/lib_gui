from PyQt5.QtCore import Qt

from ..page import Page

def switch_to_load_page(self):
    self._switch_to_page(Page.LOAD)

def cancel_load(self):
    self.switch_to_start_page()

def finished_load(self):
    self.switch_to_scanning_page()

def connect_load_buttons(self):
    self.sample_loaded_btn.clicked.connect(self.finished_load)
    self.cancel_load_btn.clicked.connect(self.cancel_load)
