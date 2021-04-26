import logging

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from .page import Page

def connect_shortcuts(self):
    """Connects all possible shortcuts"""

    self.next_shortcut = QShortcut(QKeySequence("n"), self)
    self.next_shortcut.activated.connect(self._move_to_next_screen)

    self.close_shortcut = QShortcut(QKeySequence("q"), self)
    self.close_shortcut.activated.connect(self.close)

def _move_to_next_screen(self):
    """Moves to the next screen for shortcuts"""

    if self.debug:
        index = self.stackedWidget.currentIndex()
        index += 1
        possible_indexes = {x.value: x for x in Page.__members__.values()}
        if index not in possible_indexes:
            index = 0
        logging.debug("Keyboard shortcut used to move to next screen")
        self._switch_to_page(possible_indexes[index])
    else:
        logging.warning("Keyboard shortcut was pressed but debug is not set")
