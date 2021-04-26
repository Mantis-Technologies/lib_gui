import os
import sys

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from .page import Page

class GUI(QtWidgets.QMainWindow):

    gui_ui_fname = "gui.ui"

    def __init__(self, debug=False):
        if "PYTEST_CURRENT_TEST" not in os.environ:
            self.app = QApplication(sys.argv)
        super(GUI, self).__init__()


        self.debug = debug

        self.ui = uic.loadUi(self.ui_path, self)
        print("here")
        # Connect start buttons
        self.connect_start_buttons()
        # Connect confirmation buttons
        self.connect_confirmation_buttons()
        # Connect loading sample buttons
        self.connect_load_buttons()
        # Connect results buttons
        self.connect_results_buttons()
        # Connect Order Buttons
        self.connect_order_buttons()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.set_visibility_of_prep_combo_box(visible=False)
        self.connect_shortcuts()
        self.switch_to_boot_page()

    def _switch_to_page(self, page: Page):
        if not self.debug:
            self.setCursor(Qt.BlankCursor)
        self.stackedWidget.setCurrentIndex(page.value)
        self.update()
        self.show()

        # Don't bother with this in pytest since we use pytest-qt
        if "PYTEST_CURRENT_TEST" not in os.environ:
            # If you don't do this it waits until it's completely done w callback
            # https://stackoverflow.com/a/2066916/8903959
            self.app.processEvents()
        else:
            assert self.current_page == page

    @property
    def current_page(self):
        return Page(self.stackedWidget.currentIndex())

    def close(self):
        """Closes the GUI. Done here for easy inheritance"""

        super(GUI, self).close()

    # Boot page methods
    from .pages.boot_page import switch_to_boot_page

    # Start page methods
    from .pages.start_page import switch_to_start_page
    from .pages.start_page import connect_start_buttons

    # Confirmation over 21 page methods
    from .pages.confirmation_page import switch_to_confirmation_page
    from .pages.confirmation_page import connect_confirmation_buttons

    # Order page methods
    from .pages.order_page import switch_to_order_page
    from .pages.order_page import connect_order_buttons
    from .pages.order_page import connect_num_buttons
    from .pages.order_page import connect_del_btn
    from .pages.order_page import get_order_num
    from .pages.order_page import set_order_num
    from .pages.order_page import change_order_id_lbl
    from .pages.order_page import set_visibility_of_prep_combo_box
    from .pages.order_page import get_prep

    # Loading page methods (for loading sample)
    from .pages.load_page import switch_to_load_page
    from .pages.load_page import connect_load_buttons
    from .pages.load_page import cancel_load
    from .pages.load_page import finished_load

    # Scanning page methods (while sample is being scanned)
    from .pages.scanning_page import switch_to_scanning_page

    from .pages.results_page import switch_to_results_page
    from .pages.results_page import set_results_labels
    from .pages.results_page import connect_results_buttons
    from .pages.results_page import done_w_results

    from .pages.error_page import switch_to_error_page

    from .actions import connect_shortcuts
    from .actions import _move_to_next_screen

    def run(self):

        self.showFullScreen()
        sys.exit(self.app.exec_())

    @property
    def ui_path(self):
        _dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(_dir, self.gui_ui_fname)
