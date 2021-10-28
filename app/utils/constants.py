from enum import Enum

class IntervalName(str, Enum):
    minute = '1m'
    fiveMinute = '5m'
    fifteenMinute = '15m'
    thirtyMinute = '30m'
    hour = '1h'
    day = '1d'
    week = '1w'

    @staticmethod 
    def get_mapping():
        return {
            "1 Minute": "1m",
            "5 Minutes": "5m",
            "15 Minutes": "15m",
            "30 Minutes": "30m",
            "1 Hour": "1h",
            "1 Day": "1d",
            "1 Week": "1w"
        }
