from ..page import Page

def switch_to_boot_page(self):
    self._switch_to_page(Page.BOOTING)
