from enum import Enum

class Page(Enum):
    BOOTING = 0
    START = 1
    # Over 21 page
    CONFIRMATION = 2
    ORDER = 3
    LOAD = 4
    SCANNING = 5
    RESULTS = 6
    ERROR = 7
