#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file runs the GUI with cmd line arguments"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from argparse import ArgumentParser

from .gui import GUI
from .lab_gui import LabGUI


def main():
    """Installs spectrometer with command line arguments"""

    parser = ArgumentParser(description="Runs GUI")
    parser.add_argument("--gui", default=False, action="store_true")
    parser.add_argument("--lab", default=False, action="store_true")
    # If debug is on, typing n will move to next screen, and cursor remains
    parser.add_argument("--debug", default=False, action="store_true")

    args = parser.parse_args()

    # Run the normal gui
    if args.gui:
        GUI(debug=args.debug).run()
    # Run the lab gui
    elif args.lab:
        LabGUI(debug=args.debug).run()
    else:
        parser.print_help()
