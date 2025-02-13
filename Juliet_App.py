import sys
import serial
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QPushButton, QListWidget, QLabel, QSplitter, QListWidgetItem)

from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QTimer, Qt
from PUS import *
from SPP import *
from crc import Calculator, Crc16
from cobs import cobs
from Build_UART_msg import *

class SerialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.messages = []  # Stores tuples of (raw_bytes, spp_header, pus_header)
        self.init_ui()
        self.init_serial()

    def init_ui(self):
        self.setWindowTitle("JULIET")
        main_layout = QVBoxLayout()

        # Splitter for raw messages and decoded details
        splitter = QSplitter(Qt.Horizontal)

        # Left Panel: Raw Messages
        self.msg_list = QListWidget()
        self.msg_list.itemClicked.connect(self.show_decoded_details)
        splitter.addWidget(self.msg_list)

        # Right Panel: Decoded Details
        self.details_edit = QTextEdit()
        self.details_edit.setReadOnly(True)
        splitter.addWidget(self.details_edit)

        # Buttons
        self.send_button_1 = QPushButton('Activate periodic HK data')
        self.send_button_2 = QPushButton('Activate one shot HK data')
        self.send_button_3 = QPushButton('Deactivate periodic HK data')

        # Connect buttons
        self.send_button_1.clicked.connect(
            lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID,
                                      sub_service_id=PUS_HK_Subtype_ID.HK_EN_PERIODIC_REPORTS,
                                      command_data=Command_data.HK_UC))
        self.send_button_2.clicked.connect(
            lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID,
                                      sub_service_id=PUS_HK_Subtype_ID.HK_ONE_SHOT,
                                      command_data=Command_data.HK_UC))
        self.send_button_3.clicked.connect(
            lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID,
                                      sub_service_id=PUS_HK_Subtype_ID.HK_DIS_PERIODIC_REPORTS,
                                      command_data=Command_data.HK_UC))

        # Assemble layout
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.send_button_1)
        main_layout.addWidget(self.send_button_2)
        main_layout.addWidget(self.send_button_3)
        self.setLayout(main_layout)
        self.show()

    def init_serial(self):
        self.ser = serial.Serial('COM4', baudrate=115200, timeout=1)
        self.read_thread = threading.Thread(target=self.read_serial_data, daemon=True)
        self.read_thread.start()

    def read_serial_data(self):
        buffer = bytearray()
        started = False
        while True:
            byte = self.ser.read(1)
            if byte:
                byte_value = byte[0]
                if byte_value != 0x00:
                    started = True
                if started:
                    buffer.append(byte_value)
                    if byte_value == 0x00:
                        self.messages.append(buffer)
                        hex_str = " ".join(f"0x{b:02X}" for b in buffer)

                        decoded = cobs.decode(buffer[:-1])
                        spp_header = SPP_decode(decoded[:6])
                        pus_header = PUS_TM_decode(decoded[6:15])


                        
                        if(spp_header.packet_type == 0 and pus_header.service_id == 1):
                            if(pus_header.subtype_id == 1):
                                item = QListWidgetItem(f"Received: ACK ACC OK {hex_str}")  # Create a list item
                            elif(pus_header.subtype_id == 3):
                                item = QListWidgetItem(f"Received: ACK START OK {hex_str}")  # Create a list item
                            elif(pus_header.subtype_id == 5):
                                item = QListWidgetItem(f"Received: ACK EXE OK {hex_str}")  # Create a list item
                            elif(pus_header.subtype_id == 7):
                                item = QListWidgetItem(f"Received: ACK FINISH OK {hex_str}")  # Create a list item
                            item.setForeground(QBrush(QColor("purple")))  # Set text color to blue
                        else:
                            item = QListWidgetItem(f"Received: {hex_str}")  # Create a list item
                            item.setForeground(QBrush(QColor("blue")))  # Set text color to blue
                        self.msg_list.addItem(item)

                        buffer = bytearray()
                        started = False

    def show_decoded_details(self, item):
        index = self.msg_list.row(item)
        if index >= len(self.messages):
            return  # Handle edge cases
        
        raw_bytes = self.messages[index]

        decoded = cobs.decode(raw_bytes[:-1])
        spp_header = SPP_decode(decoded[:6])
        pus_header = None

        details = []

        if spp_header:
            # details.append(str(spp_header))
            details.append("SPP Header:")
            details.append(f"  Version: {spp_header.spp_version}")
            details.append(f"  Packet Type: {spp_header.packet_type}")
            details.append(f"  Secondary Header: {spp_header.sec_head_flag}")
            details.append(f"  APID: {spp_header.apid}")
            details.append(f"  Seqeunce Flags: {spp_header.seq_flags}")
            details.append(f"  Seqeunce Count: {spp_header.sc}")
            details.append(f"  Data Length: {spp_header.data_len}")
            details.append(f"")
        else:
            details.append("SPP Header: Decode Failed")

        if spp_header.sec_head_flag:
            if spp_header.packet_type == 1:
                pus_header = PUS_TC_decode(decoded[6:15])

                details.append("\nPUS TC Header:")
                details.append(f"  PUS Version: {pus_header.pus_ver}")
                details.append(f"  Ack Flags: {pus_header.ack_flags}")
                details.append(f"  Service ID: {pus_header.service_id}")
                details.append(f"  Subtype ID: {pus_header.subtype_id}")
                details.append(f"  Source ID: {pus_header.source_id}")
                details.append(f"")
            
            elif spp_header.packet_type == 0:
                pus_header = PUS_TM_decode(decoded[6:15])

                details.append("\nPUS TM Header:")
                details.append(f"  PUS Version: {pus_header.pus_ver}")
                details.append(f"  Time Reference Status: {pus_header.sc_t_ref}")
                details.append(f"  Service ID: {pus_header.service_id}")
                details.append(f"  Subtype ID: {pus_header.subtype_id}")
                details.append(f"  Message Type Counter: {pus_header.msg_cnt}")
                details.append(f"  Destination ID: {pus_header.dest_id}")
                details.append(f"  Time: {pus_header.time}")
                details.append(f"")

            else:
                details.append("\nPUS Header: Not available or decode failed")
        
        self.details_edit.setText("\n".join(details))

    def send_command(self, service_id, sub_service_id, command_data):
        cobs_msg = build_msg_SPP_PUS_Data_CRC(service_id, sub_service_id, command_data)
        
        hex_str = " ".join(f"0x{b:02X}" for b in cobs_msg)
        self.ser.write(cobs_msg)

        self.messages.append(cobs_msg)
        item = QListWidgetItem(f"Sent: {hex_str}")  # Create a list item
        item.setForeground(QBrush(QColor("green")))  # Set text color to blue
        self.msg_list.addItem(item)

def main():
    app = QApplication(sys.argv)
    window = SerialApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()