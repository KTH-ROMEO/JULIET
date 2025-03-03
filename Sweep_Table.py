import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

class uC_Sweep_Tables:
    def __init__(self):
        self.Table = [[0] * 256 for _ in range(8)]

class FPGA_Sweep_Tables:
    def __init__(self):
        self.Table = [[0] * 256 for _ in range(2)]

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

class Excel_table:
    def __init__(self):
        self.file_path = "Sweep_Tables_Examples.xlsx"
        self.xlsx_file = pd.read_excel(self.file_path, engine='openpyxl')
        self.column_name = "Table 2"  # Change this to your actual column name
        self.data_list = self.xlsx_file[self.column_name].tolist()
        print(self.data_list)

if __name__ == "__main__":
    table = Excel_table()

