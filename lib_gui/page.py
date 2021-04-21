from enum import Enum

class Page(Enum):
    START = 0
    LOAD = 1
    SCANNING = 2
    RESULTS = 3
    MAINTENANCE = 4
    BOOTING = 5
    ERROR = 6
    # Over 21
    CONFIRMATION = 7
    ORDER = 8
    INVALID_CODE = 9
