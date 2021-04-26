from PyQt5.QtCore import Qt

from ..page import Page

def switch_to_error_page(self):
    self._switch_to_page(Page.ERROR)
