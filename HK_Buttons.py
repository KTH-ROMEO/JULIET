from PyQt5.QtWidgets import QPushButton

def get_hk_buttons(callbacks):
    """Returns a list of housekeeping buttons connected to callback functions."""
    buttons = [
        QPushButton('Activate Periodic HK MCU'),
        QPushButton('Activate Periodic HK FPGA'),
        QPushButton('Activate Periodic HK MCU & FPGA'),
        QPushButton('Deactivate Periodic HK MCU'),
        QPushButton('Deactivate Periodic HK FPGA'),
        QPushButton('Deactivate Periodic HK MCU & FPGA'),
        QPushButton('Activate Oneshot HK MCU'),
        QPushButton('Activate Oneshot HK FPGA'),
        QPushButton('Activate Oneshot HK MCU & FPGA')
    ]

    # Connect buttons to callbacks
    buttons[0].clicked.connect(lambda: callbacks['act_per_HK_uC']())
    buttons[1].clicked.connect(lambda: callbacks['act_per_HK_FPGA']())
    buttons[2].clicked.connect(lambda: callbacks['act_per_HK_uC_FPGA']())
    buttons[3].clicked.connect(lambda: callbacks['deact_per_HK_uC']())
    buttons[4].clicked.connect(lambda: callbacks['deact_per_HK_FPGA']())
    buttons[5].clicked.connect(lambda: callbacks['deact_per_HK_uC_FPGA']())
    buttons[6].clicked.connect(lambda: callbacks['oneshot_HK_uC']())
    buttons[7].clicked.connect(lambda: callbacks['oneshot_HK_FPGA']())
    buttons[8].clicked.connect(lambda: callbacks['oneshot_HK_uC_FPGA']())

    return buttons