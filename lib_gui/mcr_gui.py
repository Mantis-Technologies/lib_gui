from .gui import GUI
from .page import Page

class MCRGUI(GUI):

    def __init__(self, *args, **kwargs):
        super(MCRGUI, self).__init__(*args, **kwargs)
        self.change_order_id_lbl()
        self.set_visibility_of_prep_combo_box(visible=True)

    def switch_to_confirmation_page(self):
        self._switch_to_order_page()

    def switch_to_results_page(self):
        self._switch_to_order_page()

    def done_w_results(self):
        self._switch_to_order_page()
