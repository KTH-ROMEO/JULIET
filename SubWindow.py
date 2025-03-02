from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton

import Global_Variables

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
        
        self.setLayout(layout)
    
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

        except ValueError:
            print("Invalid input. Please enter a valid number")

