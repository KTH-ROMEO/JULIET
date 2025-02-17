import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class uC_Sweet_Tables:
    def __init__(self):
        self.Table = [[0] * 256 for _ in range(8)]

class PlotWindow(QDialog):
    def __init__(self, y, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sweep Table Voltages")
        self.resize(400, 300)
        
        # Create a vertical layout for the dialog
        layout = QVBoxLayout(self)
        
        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Plot the data
        ax = self.figure.add_subplot(111)

        x = np.arange(256)

        ax.plot(x, y)
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        ax.set_title('Array Plot')
        
        # Draw the canvas
        self.canvas.draw()