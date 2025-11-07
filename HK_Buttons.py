from PyQt5.QtWidgets import QPushButton
from SubWindow import *

def get_hk_buttons(callbacks):
    """Returns a list of housekeeping buttons connected to callback functions."""
    buttons = [
        QPushButton('Request Oneshot HK'),
        QPushButton('Set Period HK'),
        QPushButton('Get Period HK')



    ]

    # Connect buttons to callbacks
    buttons[0].clicked.connect(lambda: get_input("oneshot_HK", callbacks['oneshot_HK']))
    buttons[1].clicked.connect(lambda: get_input("set_period_HK", callbacks['set_period_HK']))
    buttons[2].clicked.connect(lambda: get_input("get_period_HK", callbacks['get_period_HK']))

    return buttons

def get_input(description, callback):
    input_window = InputWindow(description, callback)
    input_window.show()