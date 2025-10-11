from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton

import Global_Variables
import time

class ButtonWindow(QWidget):
    def __init__(self, title, buttons):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 300, 400)  # Adjust size and position

        layout = QVBoxLayout()
        
        for button in buttons:
            layout.addWidget(button)
        
        self.setLayout(layout)

class InputWindow(QWidget):
    def __init__(self, description, callback):
        super().__init__()
        self.setWindowTitle("Input Window")

        layout = QVBoxLayout()

        if description == "set_swt_MCU_v":
            Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE = 0
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Sweep Table ID: ")
            self.input_1_box = QLineEdit()

            self.input_2_button = QPushButton("Set Entire Table")
            self.input_2_button.setCheckable(True)  # Makes it toggleable

            self.input_3_label = QLabel("Step ID: ")
            self.input_3_box = QLineEdit()
            self.input_4_label = QLabel("Voltage Level: ")
            self.input_4_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.input_2_button)
            layout.addWidget(self.input_3_label)
            layout.addWidget(self.input_3_box)
            layout.addWidget(self.input_4_label)
            layout.addWidget(self.input_4_box)
            layout.addWidget(self.save_button)

            self.input_2_button.toggled.connect(self.toggle_inputs)
            self.save_button.clicked.connect(lambda: self.save_input(description, callback))
        
        elif description == "get_swt_MCU_v":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Sweep Table ID: ")
            self.input_1_box = QLineEdit()
            self.input_3_label = QLabel("Step ID: ")
            self.input_3_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)

            self.input_2_button = QPushButton("Get Entire Table")
            self.input_2_button.setCheckable(True)  # Makes it toggleable

            layout.addWidget(self.input_2_button)
            layout.addWidget(self.input_3_label)
            layout.addWidget(self.input_3_box)
            layout.addWidget(self.save_button)

            self.input_2_button.toggled.connect(self.toggle_inputs)
            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        # Create the input box for variable input
        if description == "set_CB_voltage":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Langmuir Probe ID: ")
            self.input_1_box = QLineEdit()
            self.input_2_label = QLabel("CB Mode Voltage: ")
            self.input_2_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.input_2_label)
            layout.addWidget(self.input_2_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "get_CB_voltage":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Langmuir Probe ID: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "set_whole_swt_FPGA":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Sweep Table ID: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))
        
        
        elif description == "set_swt_FPGA_v":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Sweep Table ID: ")
            self.input_1_box = QLineEdit()
            self.input_2_label = QLabel("Step ID: ")
            self.input_2_box = QLineEdit()
            self.input_3_label = QLabel("Voltage Level: ")
            self.input_3_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.input_2_label)
            layout.addWidget(self.input_2_box)
            layout.addWidget(self.input_3_label)
            layout.addWidget(self.input_3_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))
        
        elif description == "get_swt_FPGA_v":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Sweep Table ID: ")
            self.input_1_box = QLineEdit()
            self.input_2_label = QLabel("Step ID: ")
            self.input_2_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.input_2_label)
            layout.addWidget(self.input_2_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "get_whole_swt_FPGA":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Sweep Table ID: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "set_steps_SB_mode":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Number of Steps in SB Mode: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "set_samples_per_step_SB_mode":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Number of Samples per Step in SB Mode: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))
        
        elif description == "set_skipped_samples":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Number of Skipped Samples per Step in SB Mode: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))
        
        elif description == "set_samples_per_point":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Number of Samples per Point in SB Mode: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "set_points_per_step":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("Number of Points per Step in SB Mode: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))
        
        elif description == "cpy_FRAM_to_FPGA":
             # Optional: add a label for clarity
            self.input_1_label = QLabel("FRAM Sweep Table ID: ")
            self.input_1_box = QLineEdit()
            self.input_3_label = QLabel("FPGA Sweep Table ID: ")
            self.input_3_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)

            layout.addWidget(self.input_3_label)
            layout.addWidget(self.input_3_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "jump_to_image":
            self.input_1_label = QLabel("Index of desired firmware image: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))
            layout.addWidget(self.save_button)
        

        elif description == "oneshot_HK":
            self.input_1_label = QLabel("HK ID: ")
            self.input_1_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        elif description == "set_period_HK":

            self.input_1_label = QLabel("HK ID: ")
            self.input_1_box = QLineEdit()
            self.input_2_label = QLabel("Period code: ")
            self.input_2_box = QLineEdit()
            self.save_button = QPushButton("Send Command")

            layout.addWidget(self.input_1_label)
            layout.addWidget(self.input_1_box)
            layout.addWidget(self.input_2_label)
            layout.addWidget(self.input_2_box)
            layout.addWidget(self.save_button)

            self.save_button.clicked.connect(lambda: self.save_input(description, callback))

        self.setLayout(layout)

    
    def toggle_inputs(self, checked):
        """Enable/disable other input fields based on button state."""
        self.input_3_box.setDisabled(checked)
        # self.input_4_box.setDisabled(checked)
        if Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE == 0:
            Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE = 1
        else:
            Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE = 0
    
    def save_input(self, description, callback):

        try:
            if description == "set_CB_voltage":
                probe_id = self.input_1_box.text()
                voltage_value = self.input_2_box.text()
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)
                Global_Variables.CB_MODE_VOLTAGE = int(voltage_value)
                callback()

            elif description == "get_CB_voltage":
                probe_id = self.input_1_box.text()
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)
                callback()

            elif description == "set_swt_MCU_v":
                probe_id = self.input_1_box.text()
                step_id = self.input_3_box.text()
                voltage_lvl = self.input_4_box.text()

                Global_Variables.TARGET = 1
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)
                Global_Variables.SWEEP_TABLE_VOLTAGE = int(voltage_lvl)

                if Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE == 1:
                    Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE = 0
                    for i in range(0,256):
                        Global_Variables.STEP_ID = i
                        callback()
                        time.sleep(0.2)
                else:
                    Global_Variables.STEP_ID = int(step_id)
                    callback()

            elif description == "get_swt_MCU_v":
                probe_id = self.input_1_box.text()
                step_id = self.input_3_box.text()
                Global_Variables.TARGET = 1
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)

                if Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE == 1:
                    Global_Variables.APPLY_ON_ENTIRE_SWEEP_TABLE = 0
                    for i in range(0,256):
                        Global_Variables.STEP_ID = i
                        callback()
                        time.sleep(0.2)
                else:
                    Global_Variables.STEP_ID = int(step_id)
                    callback()

            elif description == "set_swt_FPGA_v":
                probe_id = self.input_1_box.text()
                step_id = self.input_2_box.text()
                voltage_lvl = self.input_3_box.text()
                Global_Variables.TARGET = 0
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)
                Global_Variables.STEP_ID = int(step_id)
                Global_Variables.SWEEP_TABLE_VOLTAGE = int(voltage_lvl)
                callback()
            
            elif description == "set_whole_swt_FPGA":
                probe_id = self.input_1_box.text()
                Global_Variables.TARGET = 0
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)
                callback()

            elif description == "get_swt_FPGA_v":
                probe_id = self.input_1_box.text()
                step_id = self.input_2_box.text()
                Global_Variables.TARGET = 0
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)
                Global_Variables.STEP_ID = int(step_id)
                callback()

            elif description == "get_whole_swt_FPGA":
                probe_id = self.input_1_box.text()
                Global_Variables.TARGET = 0
                Global_Variables.LANGMUIR_PROBE_ID = int(probe_id)
                callback()

            elif description == "set_steps_SB_mode":
                nr_of_steps = self.input_1_box.text()
                Global_Variables.SB_MODE_NR_STEPS = int(nr_of_steps)
                callback()

            elif description == "set_samples_per_step_SB_mode":
                nr_of_samples_per_step = self.input_1_box.text()
                Global_Variables.SB_MODE_NR_SAMPLES_PER_STEP = int(nr_of_samples_per_step)
                callback()

            elif description == "set_skipped_samples":
                skipped_samples = self.input_1_box.text()
                Global_Variables.SB_MODE_NR_SKIPPED_SAMPLES = int(skipped_samples)
                callback()
            
            elif description == "set_samples_per_point":
                samples_per_point = self.input_1_box.text()
                Global_Variables.SB_MODE_NR_SAMPLES_PER_POINT = int(samples_per_point)
                callback()

            elif description == "set_points_per_step":
                points_per_step = self.input_1_box.text()
                Global_Variables.SB_MODE_NR_POINTS_PER_STEP = int(points_per_step)
                callback()

            elif description == "cpy_FRAM_to_FPGA":
                FRAM_swt_id = self.input_1_box.text()
                FPGA_swt_id = self.input_3_box.text()
                Global_Variables.FRAM_TABLE_ID = int(FRAM_swt_id)
                Global_Variables.LANGMUIR_PROBE_ID = int(FPGA_swt_id)
                callback()

            elif description == "jump_to_image":
                Image_index = self.input_1_box.text()
                Global_Variables.IMAGE_INDEX = int(Image_index)
                callback()


            elif description == "oneshot_HK":
                hk_id = self.input_1_box.text()
                Global_Variables.HK_ID = int(hk_id)
                callback()


            elif description == "set_period_HK":
                hk_id = self.input_1_box.text()
                hk_period = self.input_2_box.text()
                Global_Variables.HK_ID = int(hk_id)
                Global_Variables.HK_PERIOD = int(hk_period)
                callback()


        except ValueError:
            print("Invalid input. Please enter a valid number")

