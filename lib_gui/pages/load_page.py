from PyQt5.QtCore import Qt

from ..page import Page

def switch_to_load_page(self):
    self._switch_to_page(Page.LOAD)

def cancel_load(self):
    self.switch_to_start_page()

def finished_load(self):
    self.switch_to_scanning_page()

def connect_load_buttons(self):
    self.SampleLoadedBTN.clicked.connect(self.finished_load)
    self.CancelLoadingBTN.clicked.connect(self.cancel_load)
