from PyQt5.QtWidgets import QPushButton

def get_sweep_table_MCU_buttons(callbacks):
    """Returns a list of sweep table buttons connected to callback functions."""
    buttons = [
        QPushButton('Sweep Table 1'),
        QPushButton('Sweep Table 2'),
        QPushButton('Sweep Table 3'),
        QPushButton('Sweep Table 4'),
        QPushButton('Sweep Table 5'),
        QPushButton('Sweep Table 6'),
        QPushButton('Sweep Table 7'),
        QPushButton('Sweep Table 8'),
    ]

    # Connect buttons to callbacks
    buttons[0].clicked.connect(lambda: callbacks['uC_SW_T_1']())
    buttons[1].clicked.connect(lambda: callbacks['uC_SW_T_2']())
    buttons[2].clicked.connect(lambda: callbacks['uC_SW_T_3']())
    buttons[3].clicked.connect(lambda: callbacks['uC_SW_T_4']())
    buttons[4].clicked.connect(lambda: callbacks['uC_SW_T_5']())
    buttons[5].clicked.connect(lambda: callbacks['uC_SW_T_6']())
    buttons[6].clicked.connect(lambda: callbacks['uC_SW_T_7']())
    buttons[7].clicked.connect(lambda: callbacks['uC_SW_T_8']())

    return buttons