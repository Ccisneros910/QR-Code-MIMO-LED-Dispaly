#QR_DICTIONARIES.py
"""File provides reference dictionaries and constants for metrics of QR code versions.
For use with QR LED Link Library."""

#####Constants#####

BUF_SIZE = 100000

#####Dictionaries######

VERSION_SIZE = {
    1 : "21",
    2 : "25",
    3 : "29",
    4 : "33"
}

QR_DICT_L = {
    "21" : 25,
    "25" : 47,
    "29" : 77,
    "33" : 114
}

QR_DICT_M = {
    "21": 20,
    "25": 38,
    "29": 61,
    "33": 90
}

QR_DICT_Q = {
    "21": 16,
    "25": 29,
    "29": 47,
    "33": 67
}

QR_DICT_H = {
    "21": 10,
    "25": 20,
    "29": 35,
    "33": 50
}
