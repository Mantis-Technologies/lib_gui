#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains the methods relating to the FAQ page"""

__author__ = "Michael Mahoney"
__credits__ = ["Michael Mahoney"]
__maintainer__ = "Michael Mahoney"
__email__ = "mike@cannacheckkiosk.com"

from ..page import Page
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QWidget, QSizePolicy
from PyQt5.QtGui import QPixmap
import time
import os


def switch_to_faq_page(self):
    """Switches to the FAQ page"""
    self._switch_to_page(Page.FAQ)
    self.FAQPageTimeoutThread = FAQPageTimeoutThread(self)
    self.FAQPageTimeoutThread.signal.connect(self.FAQPageTimeoutCallback)
    self.FAQPageTimeoutThread.start()


def connect_faq_buttons(self):
    """Connects FAQ buttons"""
    self.ui.faq_back_btn.clicked.connect(self.faq_back_to_start_page)


def faq_back_to_start_page(self):
    self.FAQPageTimeoutThread.keepRunning = False
    self.reset_faq_page()
    self.switch_to_start_page()


def FAQPageTimeoutCallback(self, result):
    self.faq_back_to_start_page()


def reset_faq_page(self):
    """Reset the FAQ page to its initial state"""
    self.ui.faq_scroll_area.verticalScrollBar().setValue(0)  # Reset scroll to top
    for faq in self.faq_buttons:
        faq["button"].setChecked(False)
        faq["answer_label"].setVisible(False)
        for image_layout in faq["image_layouts"]:
            for i in range(image_layout.count()):
                item_layout = image_layout.itemAt(i).layout()
                image_label = item_layout.itemAt(0).widget()
                desc_label = item_layout.itemAt(1).widget()
                image_label.setVisible(False)
                desc_label.setVisible(False)


class FAQPageTimeoutThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui
        self.keepRunning = True

    def run(self):
        maxSecondsToWait = 300  # allow the user 5 minutes to read the page or revert back
        while self.keepRunning and self.gui.keepThreadsRunning:
            maxSecondsToWait = maxSecondsToWait - 1
            if maxSecondsToWait == 0:
                self.signal.emit(1)  # emit anything to trigger page change
                break
            time.sleep(1)


def setup_faq_page(self, ui_version):
    """Set up the FAQ page with questions and answers"""
    faqs = [
        ("What is a CannaCheck™ Kiosk?", "A CannaCheck™ Kiosk is a self-service machine for cannabis testing."),
        ("How does it work?", "The kiosk uses advanced NIR spectroscopy to analyze cannabis samples."),
        ("How does NIR spectroscopy work?", "NIR spectroscopy works by shining near-infrared light onto a sample. The light is absorbed by the sample at specific wavelengths, creating a unique spectral fingerprint that can be analyzed to determine the composition and properties of the sample."),
        ("What other industries use NIR spectroscopy?", "NIR spectroscopy technology is used in industries such as big agriculture, pharmaceuticals, and food & beverage."),
        ("How accurate is CannaCheck™'s kiosk?", "The kiosk provides highly accurate results comparable to lab tests. The machine is accurate to +/-10% of the measured value. For example, on a 20% THC-A flower, the variance would be +/-2%. This means the flower would be within 18% to 22% THC-A."),
        ("How is total THC and total CBD calculated?", "Total THC and Total CBD are calculated using specific equations that account for both the acidic and neutral forms of these cannabinoids. The equations are as follows:\n\nTotal THC = (THC-A * 0.877) + THC\nTotal CBD = (CBD-A * 0.877) + CBD\n\nThese calculations are based on the fact that THC-A and CBD-A, the acidic forms, convert to their neutral forms (THC and CBD) when heated. The conversion factor 0.877 accounts for the loss of the carboxyl group during this process. These equations provide a more comprehensive measure of the total potential content of THC and CBD in the sample."),
        ("Why do samples from the same plant show different results?", "\nVariations can occur due to differences in sample preparation and environmental factors. Environmental factors are the most prevalent, primarily due to the natural variance in cannabis flower itself. Examples of variations in sample preparation include differing levels of fineness in the ground flower, holes where light can shine through the sample, or dirty sample cups, such as sample cups with fingerprints on the bottom.\n"),
        ("Why do I get different results when I retest the same sample?", "\nEven when retesting the exact same sample, variations can occur due to several factors. Touching the bottom of the sample cup when removing the sample, jostling the sample when reinserting it, and fingerprint oils on the sample cup can all affect the results. Additionally, slight changes in temperature and moisture can impact the readings. Because the machine only tests a 14mm diameter of a 47mm cup, and cannabis is naturally highly variable, different parts of the same sample can yield different results.\n"),
        ("How do I get the most consistent results?", "Ensure consistent sample preparation and handling of the sample cups for best results. If retesting a sample, average the differences between tests to understand the most representative value."),
        ("Why grind the sample?", "Grinding the sample ensures a uniform and representative sample for analysis."),
        ("Does the sample weight matter for accurate results with NIR?", "Yes, the weight of the sample does matter for accurate results with NIR spectroscopy. However, when testing a small portion of a much larger sample, like CannaCheck™'s method, the weight is not critical as long as the sample completely fills the cup to ensure no light passes through. Consistency in sample preparation is key."),
        ("Can CannaCheck™ measure extracts?", "No, CannaCheck™ cannot measure extracts at this time."),
        ("Can CannaCheck™ measure edibles or infused products?", "Currently, CannaCheck™ is not designed to measure edibles or infused products due to many other ingredients obscuring the optical sampling process."),
        ("Can CannaCheck™ measure contaminants (pesticides, molds etc)?", "CannaCheck™ cannot detect certain contaminants at meaningful levels, as it is primarily designed for potency testing."),
        ("Can CannaCheck™ measure heavy metals?", "No, CannaCheck™ does not measure heavy metals."),
        ("Can CannaCheck™ measure terpenes?", "No, at this time, CannaCheck™ cannot measure terpenes."),
        ("Is CannaCheck™ a state-certified test method?", "No. Most states name only HPLC or GC as certified methods. The CannaCheck™ is not intended to replace mandatory third-party testing of final product. It is only intended to replace R&D testing which does not require HPLC or GC."),
        ("What are optimal use-cases for CannaCheck™?", "Any time a potency measurement is needed that doesn’t require third-party lab testing. Pheno hunting, optimization of cultivation parameters, R&D testing, dosing of edibles, and more. CannaCheck™ is made for home growers to receive testing with far greater accuracy and precision than competing products at an accessible price point."),
        ("Is CannaCheck™ supposed to eliminate outside lab-testing?", "No, CannaCheck™ is designed to complement outside lab-testing."),
        ("What can CannaCheck™ test for?", "CannaCheck™ can test for THC-A, CBD-A, THC, CBD, Total THC, and Total CBD."),
        ("How is CannaCheck™ different than HPLC or GC?", "CannaCheck™ uses spectroscopy, which is faster and less expensive than HPLC or GC."),
        ("Will CannaCheck™ results match my lab results?", "CannaCheck™ results are highly accurate and comparable to lab values, but slight variations may occur due to sample preparation, sample size, natural variance, and other factors."),
    ]

    faq_page_widget = self.stackedWidget.widget(Page.FAQ.value)
    faq_page_widget.setStyleSheet("background-color: #1b1b1b;")

    # Create a container widget for centering the scroll area
    container_widget = QWidget(faq_page_widget)

    # V2 Kiosk
    if ui_version == "gui.ui":
        container_widget.setGeometry(350, 250, 1200, 700)  # x, y, width, height
    #V3 Kiosk
    elif ui_version == "gui_v3.ui":
        container_widget.setGeometry(0, 225, 1090, 1400)  # x, y, width, height

    container_layout = QVBoxLayout(container_widget)
    container_layout.setContentsMargins(20, 20, 20, 20)  # Add margins for a nicer look
    container_widget.setStyleSheet("border-radius: 10px;")

    # Create a scroll area
    self.ui.faq_scroll_area = QScrollArea(container_widget)
    self.ui.faq_scroll_area.setWidgetResizable(True)
    self.ui.faq_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.ui.faq_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.ui.faq_scroll_area.setStyleSheet("""
        QScrollArea {
            background-color: #2e2e2e;
            border: 2px solid #444;
            border-radius: 10px;
            padding: 10px;  /* Add padding to avoid content cutting off */
        }
    """)

    # Create a widget for the scroll area contents
    scroll_content = QWidget()
    scroll_content.setStyleSheet("background-color: #2e2e2e; border-radius: 10px;")
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_layout.setAlignment(Qt.AlignTop)

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(script_dir, "..", "faq_graph_images")

    # Store FAQ buttons and layouts for reset purposes
    self.faq_buttons = []

    # Add FAQs to the scroll area content
    for question, answer in faqs:
        if question == "How accurate is CannaCheck™'s kiosk?":
            faq_data = self.add_faq(scroll_layout, question, answer, image_paths=[
                (os.path.join(image_dir, "THCtot Scatter copy.png"), "THC Total Scatter (x: actual, y: predicted)"),
                (os.path.join(image_dir, "CBDtit Scatter copy.png"), "CBD Total Scatter (x: actual, y: predicted)"),
                (os.path.join(image_dir, "Trip Scatter THC copy.png"), "Triplicate Scatter THC (x: actual, y: predicted)"),
                (os.path.join(image_dir, "Trip Scatter CBD copy.png"), "Triplicate Scatter CBD (x: actual, y: predicted)"),
                (os.path.join(image_dir, "PLS Val Errors copy.png"), "PLS Validation Errors (deviation count from zero % error)")
            ])
        else:
            faq_data = self.add_faq(scroll_layout, question, answer)
        self.faq_buttons.append(faq_data)

    self.ui.faq_scroll_area.setWidget(scroll_content)
    container_layout.addWidget(self.ui.faq_scroll_area)


def add_faq(self, layout, question, answer, image_paths=None):
    # Create question button
    question_button = QPushButton(question)
    question_button.setCheckable(True)
    question_button.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-size: 24px;
            text-align: left;
            padding: 15px;  /* Increased padding for better visibility */
            border: none;
            border-radius: 5px;
        }
        QPushButton:checked {
            background-color: #666;
        }
    """)
    question_button.clicked.connect(lambda: self.toggle_answer(answer_label, question_button, image_layouts))

    # Create answer label
    answer_label = QLabel(answer)
    answer_label.setStyleSheet("""
        QLabel {
            background-color: #2e2e2e;
            color: white;
            font-size: 22px;
            padding: 15px;  /* Increased padding for better visibility */
            border-radius: 5px;
        }
    """)
    answer_label.setWordWrap(True)
    answer_label.setVisible(False)
    answer_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    layout.addWidget(question_button)
    layout.addWidget(answer_label)

    # Create image labels if image paths are provided
    image_layouts = []
    if image_paths:
        for i in range(0, len(image_paths), 2):
            h_layout = QHBoxLayout()
            for j in range(2):
                if i + j < len(image_paths):
                    image_path, image_desc = image_paths[i + j]
                    # print(f"Attempting to load image at {image_path}")  # Debug print
                    # if os.path.exists(image_path):
                    #     print(f"Image exists at {image_path}")  # Debug print
                    # else:
                    #     print(f"Image does not exist at {image_path}")  # Debug print
                    image_label = QLabel()
                    pixmap = QPixmap(image_path)
                    # if pixmap.isNull():
                    #     print(f"Failed to load image at {image_path}")
                    # else:
                    #     print(f"Successfully loaded image at {image_path} with size {pixmap.size()}")
                    image_label.setPixmap(
                        pixmap.scaledToWidth(500, Qt.SmoothTransformation))  # Adjust width to fit better
                    image_label.setVisible(False)

                    # Create description label
                    desc_label = QLabel(image_desc)
                    desc_label.setStyleSheet("color: white; font-size: 12px; padding-top: 5px;")
                    desc_label.setAlignment(Qt.AlignCenter)
                    desc_label.setVisible(False)

                    v_layout = QVBoxLayout()
                    v_layout.addWidget(image_label)
                    v_layout.addWidget(desc_label)
                    v_layout.setAlignment(Qt.AlignHCenter)  # Center-align the vertical layout

                    h_layout.addLayout(v_layout)
            image_layouts.append(h_layout)
            layout.addLayout(h_layout)

    return {"button": question_button, "answer_label": answer_label, "image_layouts": image_layouts}


def toggle_answer(self, answer_label, question_button, image_layouts=None):
    answer_label.setVisible(not answer_label.isVisible())
    question_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    if answer_label.isVisible():
        answer_label.setFixedHeight(answer_label.sizeHint().height())
        if image_layouts:
            for image_layout in image_layouts:
                for i in range(image_layout.count()):
                    item_layout = image_layout.itemAt(i).layout()  # Changed from .widget() to .layout()
                    image_label = item_layout.itemAt(0).widget()
                    desc_label = item_layout.itemAt(1).widget()
                    # print(f"Showing image of size {image_label.sizeHint()}")  # Debug print
                    image_label.setVisible(True)
                    image_label.setFixedHeight(image_label.sizeHint().height())
                    desc_label.setVisible(True)
                    desc_label.setFixedHeight(desc_label.sizeHint().height())
    else:
        answer_label.setFixedHeight(0)
        if image_layouts:
            for image_layout in image_layouts:
                for i in range(image_layout.count()):
                    item_layout = image_layout.itemAt(i).layout()  # Changed from .widget() to .layout()
                    image_label = item_layout.itemAt(0).widget()
                    desc_label = item_layout.itemAt(1).widget()
                    image_label.setVisible(False)
                    image_label.setFixedHeight(0)
                    desc_label.setVisible(False)
                    desc_label.setFixedHeight(0)
    self.stackedWidget.widget(Page.FAQ.value).updateGeometry()
