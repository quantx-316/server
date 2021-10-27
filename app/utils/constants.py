from enum import Enum

class IntervalName(str, Enum):
    minute = '1m'
    fiveMinute = '5m'
    fifteenMinute = '15m'
    thirtyMinute = '30m'
    hour = '1h'
    day = '1d'
    week = '1w'
