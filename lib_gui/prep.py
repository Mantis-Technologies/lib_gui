#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains an enum for all preparation methods"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"

from enum import Enum


class Prep(Enum):
    """Possible methods for how a sample was prepared"""

    HAND_GRIND = 0
    MECHANICAL_GRIND = 1
    INTACT = 2


# Assert these are unique for the database
vals = list([x.value for x in Prep.__members__.values()])
assert len(set(vals)) == len(vals), "Must be unique for db"
