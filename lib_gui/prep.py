from enum import Enum


class Prep(Enum):
    HAND_GRIND = 0
    MECHANICAL_GRIND = 1
    INTACT = 2

vals = list([x.value for x in Prep.__members__.values()])
assert len(set(vals)) == len(vals), "Must be unique for db"
