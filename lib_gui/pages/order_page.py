from PyQt5.QtCore import Qt

from ..page import Page
#from ..prep import Prep

def switch_to_order_page(self):
    self.OrderNumEntry.clear()
    self._switch_to_page(Page.ORDER)

def connect_order_buttons(self):
    self.connect_num_buttons()
    self.connect_del_btn()
    def next_page():
        if len(self.get_order_num()) > 0:
            self.switch_to_load_page()
    self.OrderNumNextBTN.clicked.connect(next_page)
    self.CancelOrderNumBTN.clicked.connect(self.switch_to_start_page)

def connect_num_buttons(self):
    num_btns = [self.OneBTN, self.TwoBTN, self.ThreeBTN, self.FourBTN,
                self.FiveBTN, self.SixBTN, self.SevenBTN, self.EightBTN,
                self.NineBTN]
    # NOTE: for some reason this fails in a loop.
    # No clue why, but no time to investigate
    # So I have coded it as such

    self.OneBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.OneBTN.text()))
    self.TwoBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.TwoBTN.text()))
    self.ThreeBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.ThreeBTN.text()))
    self.FourBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.FourBTN.text()))
    self.FiveBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.FiveBTN.text()))
    self.SixBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.SixBTN.text()))
    self.SevenBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.SevenBTN.text()))
    self.EightBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.EightBTN.text()))
    self.NineBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.NineBTN.text()))
    self.ZeroBTN.clicked.connect(lambda: self.set_order_num(
        self.get_order_num() + self.ZeroBTN.text()))

def connect_del_btn(self):
    def func():
        self.set_order_num(self.get_order_num()[:-1])
    self.DelBTN.clicked.connect(func)

def get_order_num(self):
    return self.OrderNumEntry.text()

def set_order_num(self, num: str):
    assert isinstance(num, str)
    return self.OrderNumEntry.setText(num)

def change_order_id_lbl(self):
    """Changes order id for mcr lab techs"""

    self.enter_id_lbl.setText("Enter sample ID")

def remove_order_id_cancel(self):
    self.CancelOrderNumBTN.setVisible(False)

def get_prep(self):
    text = self.comboBox.currentText()
    if "mechanical grind" in text.lower():
        return Prep.MECHANICAL_GRIND
    elif "ground by hand" in text.lower():
        return Prep.HAND_GRIND
    elif "flower intact" in text.lower():
        return Prep.INTACT
    else:
        raise NotImplementedError
