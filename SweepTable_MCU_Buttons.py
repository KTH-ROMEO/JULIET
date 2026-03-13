from PyQt5.QtWidgets import QPushButton

def get_sweep_table_buttons(callbacks):
    """Returns a list of sweep table buttons connected to callback functions."""
    buttons = [
        QPushButton('Sweep Table FPGA 1'),
        QPushButton('Sweep Table FPGA 2'),
        QPushButton('Sweep Table MUC 1'),
        QPushButton('Sweep Table MUC 2'),
        QPushButton('Sweep Table MUC 3'),
        QPushButton('Sweep Table MUC 4'),
        QPushButton('Sweep Table MUC 5'),
        QPushButton('Sweep Table MUC 6'),
        QPushButton('Sweep Table MUC 7'),
        QPushButton('Sweep Table MUC 8'),
    ]

    # Connect buttons to callbacks
    buttons[0].clicked.connect(lambda: callbacks['SW_T_1']())
    buttons[1].clicked.connect(lambda: callbacks['SW_T_2']())
    buttons[2].clicked.connect(lambda: callbacks['SW_T_3']())
    buttons[3].clicked.connect(lambda: callbacks['SW_T_4']())
    buttons[4].clicked.connect(lambda: callbacks['SW_T_5']())
    buttons[5].clicked.connect(lambda: callbacks['SW_T_6']())
    buttons[6].clicked.connect(lambda: callbacks['SW_T_7']())
    buttons[7].clicked.connect(lambda: callbacks['SW_T_8']())
    buttons[8].clicked.connect(lambda: callbacks['SW_T_9']())
    buttons[9].clicked.connect(lambda: callbacks['SW_T_10']())

    return buttons
