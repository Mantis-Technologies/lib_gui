from ..page import Page


def switch_to_results_page(self):
    self._switch_to_page(Page.RESULTS)

def set_results_labels(self, analytes):
    for lbl in [self.results_1_lbl, self.results_2_lbl, self.results_3_lbl,
                self.results_4_lbl, self.results_5_lbl, self.results_6_lbl]:
        lbl.setText("")
 
    self.results_1_lbl.setText(str(analytes[0]))
    self.results_1_lbl.setStyleSheet("color:black")

def done_w_results(self):
    self.switch_to_start_page()

def connect_results_buttons(self):
    self.finished_test_btn.clicked.connect(self.done_w_results)
