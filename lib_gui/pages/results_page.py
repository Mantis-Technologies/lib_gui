from ..page import Page


def switch_to_results_page(self):
    self._switch_to_page(Page.RESULTS)

def set_results_labels(self, analytes):
    for Lbl in [self.Results1LBL, self.Results2LBL, self.Results3LBL,
                self.Results4LBL, self.Results5LBL, self.Results6LBL]:
        Lbl.setText("")
 
    self.Results1LBL.setText(str(analytes[0]))
    self.Results1LBL.setStyleSheet("color:black")

def done_w_results(self):
    self.switch_to_start_page()

def connect_results_buttons(self):
    self.FinishedTestBTN.clicked.connect(self.done_w_results)
