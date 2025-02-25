from PyQt5.QtWidgets import QPushButton

def get_fm_buttons(callbacks):
    """Returns a list of function management buttons connected to callback functions."""
    buttons = [
        QPushButton('Set MCU Sweep Table'),
        QPushButton('Get MCU Sweep Table'),
        QPushButton('Set CB Mode Voltage'),
        QPushButton('Get CB Mode Voltage'),
        QPushButton('Set FPGA Sweep Table Voltage'),
        QPushButton('Get FPGA Sweep Table Voltage')
    ]

    # Connect buttons to callbacks
    buttons[0].clicked.connect(lambda: callbacks['set_swt_MCU']())
    buttons[1].clicked.connect(lambda: callbacks['get_swt_FPGA']())
    buttons[2].clicked.connect(lambda: callbacks['set_CB_voltage']())
    buttons[3].clicked.connect(lambda: callbacks['get_CB_voltage']())
    buttons[4].clicked.connect(lambda: callbacks['set_swt_FPGA_v']())
    buttons[5].clicked.connect(lambda: callbacks['get_swt_FPGA_v']())

    return buttons