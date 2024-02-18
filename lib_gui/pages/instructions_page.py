#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..page import Page


def switch_to_instruction_page(self):
    """Switches to the instruction page"""
    self._switch_to_page(Page.INSTRUCTIONS)


def cancel_button_instruction(self):
    self.switch_to_start_page()


def next_button_instruction(self):
    self.switch_to_load_page()


def connect_instruction_buttons(self):
    self.instruction_next.clicked.connect(self.next_button_instruction)
    self.instruction_cancel.clicked.connect(self.cancel_button_instruction)