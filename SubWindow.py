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

         # Optional: add a label for clarity
        self.input_label = QLabel(description)
        layout.addWidget(self.input_label)
        
        # Create the input box for variable input
        self.input_box = QLineEdit()
        layout.addWidget(self.input_box)

        self.save_button = QPushButton("Send Command")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(lambda: self.save_input(description, callback))
        
        self.setLayout(layout)
    
    def save_input(self, description, callback):

        input_text = self.input_box.text()
        try:
            if description == "CB Mode Voltage":
                Global_Variables.CB_MODE_VOLTAGE = int(input_text)
                print(description, Global_Variables.CB_MODE_VOLTAGE)
                callback()
        except ValueError:
            print("Invalid input. Please enter a valid number")

