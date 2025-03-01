from PyQt5.QtWidgets import QPushButton
from SubWindow import *

def get_fm_buttons(callbacks):
    """Returns a list of function management buttons connected to callback functions."""
    buttons = [
        QPushButton('Set MCU Sweep Table Voltage'),
        QPushButton('Get MCU Sweep Table Voltage'),
        QPushButton('Set CB Mode Voltage'),
        QPushButton('Get CB Mode Voltage'),
        QPushButton('Set FPGA Sweep Table Voltage'),
        QPushButton('Get FPGA Sweep Table Voltage'),
        QPushButton('Set Steps of SB mode'),
        QPushButton('Get Steps of SB mode'),
        QPushButton('Set Samples per Step'),
        QPushButton('Get Samples per Step'),
        QPushButton('Set Nr of Skipped Samples'),
        QPushButton('Get Nr of Skipped Samples'),
        QPushButton('Set Samples per point'),
        QPushButton('Get Samples per point'),
        QPushButton('Set Points per Step'),
        QPushButton('Get Points per Step'),
    ]

    # Connect buttons to callbacks
    buttons[0].clicked.connect(lambda: callbacks['set_swt_MCU']())
    buttons[1].clicked.connect(lambda: callbacks['get_swt_MCU']())
    buttons[2].clicked.connect(lambda: get_input("CB Mode Voltage", callbacks['set_CB_voltage']))
    buttons[3].clicked.connect(lambda: callbacks['get_CB_voltage']())
    buttons[4].clicked.connect(lambda: callbacks['set_swt_FPGA_v']())
    buttons[5].clicked.connect(lambda: callbacks['get_swt_FPGA_v']())
    buttons[6].clicked.connect(lambda: callbacks['set_steps_SB_mode']())
    buttons[7].clicked.connect(lambda: callbacks['get_steps_SB_mode']())
    buttons[8].clicked.connect(lambda: callbacks['set_samples_per_step_SB_mode']())
    buttons[9].clicked.connect(lambda: callbacks['get_samples_per_step_SB_mode']())
    buttons[10].clicked.connect(lambda: callbacks['set_skipped_samples']())
    buttons[11].clicked.connect(lambda: callbacks['get_skipped_samples']())
    buttons[12].clicked.connect(lambda: callbacks['set_samples_per_point']())
    buttons[13].clicked.connect(lambda: callbacks['get_samples_per_point']())
    buttons[14].clicked.connect(lambda: callbacks['set_points_per_step']())
    buttons[15].clicked.connect(lambda: callbacks['get_points_per_step']())

    return buttons

def get_input(description, callback):
    input_window = InputWindow(description, callback)
    input_window.show()