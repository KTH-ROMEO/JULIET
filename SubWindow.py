from PyQt5.QtWidgets import QWidget, QVBoxLayout

class SubWindow(QWidget):
    def __init__(self, title, buttons):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 300, 400)  # Adjust size and position

        layout = QVBoxLayout()
        
        for button in buttons:
            layout.addWidget(button)
        
        self.setLayout(layout)
