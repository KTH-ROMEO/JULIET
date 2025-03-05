import sys
import serial
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QPushButton, QListWidget, QLabel, QSplitter, QListWidgetItem, QGridLayout)

from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QTimer, Qt
from PUS import *
from SPP import *
from crc import Calculator, Crc16
from cobs import cobs
from Build_UART_msg import *
from Decode_Msg import *
from Sweep_Table import *
from SubWindow import *
from HK_Buttons import *
from SweepTable_MCU_Buttons import *
from FM_Buttons import *

class SerialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.messages = []  # Stores tuples of (raw_bytes, spp_header, pus_header)
        self.init_ui()
        self.init_serial()
        self.uC_Sweep_Tables = uC_Sweep_Tables()
        self.FPGA_Sweep_Tables = FPGA_Sweep_Tables()

    def init_ui(self):
        self.setWindowTitle("JULIET")
        main_layout = QGridLayout()

        # Splitter for raw messages and decoded details
        splitter1 = QSplitter(Qt.Horizontal)

        # Left Panel: Raw Messages
        self.msg_list = QListWidget()
        self.msg_list.itemClicked.connect(self.show_decoded_details)
        splitter1.addWidget(self.msg_list)

        # Right Panel: Decoded Details
        self.details_edit = QTextEdit()
        self.details_edit.setReadOnly(True)
        splitter1.addWidget(self.details_edit)

        self.hk_button = QPushButton('Housekeeping Commands')
        self.sweep_tables_MCU = QPushButton('Sweep Tables MCU')
        self.sweep_tables_FPGA = QPushButton('Sweep Tables FPGA')
        self.fm_button = QPushButton('FM Commands')
        self.clear_button = QPushButton('Clear Console')
        self.test_button = QPushButton('Test Command')

        # Connect main buttons to actions
        self.test_button.clicked.connect(
            lambda: self.send_command(service_id=PUS_Service_ID.TEST_SERVICE_ID.value,
                                      sub_service_id=PUS_TEST_Subtype_ID.T_ARE_YOU_ALIVE_TEST_ID.value,
                                      command_data=Command_data.TS_EMPTY.value))
        self.hk_button.clicked.connect(self.show_hk_commands)
        self.sweep_tables_MCU.clicked.connect(self.show_sweep_tables_MCU)
        self.sweep_tables_FPGA.clicked.connect(self.show_sweep_tables_FPGA)
        self.fm_button.clicked.connect(self.show_FM_commands)
        self.clear_button.clicked.connect(lambda: self.clear_console())

        main_layout.addWidget(self.test_button, 0, 0, 1, 1)
        main_layout.addWidget(self.hk_button, 0, 1, 1, 1)
        main_layout.addWidget(self.fm_button, 0, 2, 1, 1)
        main_layout.addWidget(self.sweep_tables_MCU, 0, 3, 1, 1)
        main_layout.addWidget(self.sweep_tables_FPGA, 0, 4, 1, 1)
        main_layout.addWidget(self.clear_button, 0, 5, 1, 1)

        main_layout.addWidget(splitter1, 1, 0, 1, 6)

        self.setLayout(main_layout)
        self.show()

    def show_hk_commands(self):
        callbacks = {
            'act_per_HK_uC' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_EN_PERIODIC_REPORTS.value,
                                    command_data=Command_data.HK_UC.value),

            'act_per_HK_FPGA' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_EN_PERIODIC_REPORTS.value,
                                    command_data=Command_data.HK_FPGA.value),

            'act_per_HK_uC_FPGA' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_EN_PERIODIC_REPORTS.value,
                                    command_data=Command_data.HK_UC_FPGA.value),

            'oneshot_HK_uC' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_ONE_SHOT.value,
                                    command_data=Command_data.HK_UC.value),

            'oneshot_HK_FPGA' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_ONE_SHOT.value,
                                    command_data=Command_data.HK_FPGA.value),

            'oneshot_HK_uC_FPGA' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_ONE_SHOT.value,
                                    command_data=Command_data.HK_UC_FPGA.value),

            'deact_per_HK_uC' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_DIS_PERIODIC_REPORTS.value,
                                    command_data=Command_data.HK_UC.value),

            'deact_per_HK_FPGA' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_DIS_PERIODIC_REPORTS.value,
                                    command_data=Command_data.HK_FPGA.value),

            'deact_per_HK_uC_FPGA' : lambda: self.send_command(service_id=PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value,
                                    sub_service_id=PUS_HK_Subtype_ID.HK_DIS_PERIODIC_REPORTS.value,
                                    command_data=Command_data.HK_UC_FPGA.value),
        }
        self.hk_window = ButtonWindow("Housekeeping Commands", get_hk_buttons(callbacks))
        self.hk_window.show()  # Use show() instead of exec_()

    def show_sweep_tables_MCU(self):
        callbacks = {
            'uC_SW_T_1' : lambda: self.show_sw_table(0, "mcu"), 
            'uC_SW_T_2' : lambda: self.show_sw_table(1, "mcu"),
            'uC_SW_T_3' : lambda: self.show_sw_table(2, "mcu"),
            'uC_SW_T_4' : lambda: self.show_sw_table(3, "mcu"),
            'uC_SW_T_5' : lambda: self.show_sw_table(4, "mcu"),
            'uC_SW_T_6' : lambda: self.show_sw_table(5, "mcu"),
            'uC_SW_T_7' : lambda: self.show_sw_table(6, "mcu"),
            'uC_SW_T_8' : lambda: self.show_sw_table(7, "mcu"),
        }
        self.swt_mcu_window = ButtonWindow("MCU Sweep Tables", get_sweep_table_MCU_buttons(callbacks))
        self.swt_mcu_window.show()

    def show_sweep_tables_FPGA(self):
        callbacks = {
            'FPGA_SW_T_1' : lambda: self.show_sw_table(0, "fpga"), 
            'FPGA_SW_T_2' : lambda: self.show_sw_table(1, "fpga"),
        }
        self.swt_mcu_window = ButtonWindow("FPGA Sweep Tables", get_sweep_table_FPGA_buttons(callbacks))
        self.swt_mcu_window.show()

    def show_FM_commands(self):
        callbacks = {
            'set_swt_MCU_v' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_VOLTAGE_LEVEL_SWEEP_TABLE()),

            'get_swt_MCU_v' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_VOLTAGE_LEVEL_SWEEP_TABLE()),

            'set_CB_voltage' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_CONSTANT_BIAS_VOLTAGE()),

            'get_CB_voltage' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_CURRENT_CONSTANT_BIAS_VALUE()),

            'set_swt_FPGA_v' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_VOLTAGE_LEVEL_SWEEP_TABLE()),

            'get_swt_FPGA_v' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_VOLTAGE_LEVEL_SWEEP_TABLE()),

            'set_steps_SB_mode' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_STEPS_SB_MODE()),

            'get_steps_SB_mode' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_STEPS_SB_MODE()),

            'set_samples_per_step_SB_mode' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_SAMPLES_PER_STEP_SB_MODE()),

            'get_samples_per_step_SB_mode' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_SAMPLES_PER_STEP_SB_MODE()),

            'set_skipped_samples' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_SKIPPED_SAMPLES_SB_MODE()),

            'get_skipped_samples' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_SKIPPED_SAMPLES_SB_MODE()),

            'set_samples_per_point' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_SAMPLES_PER_POINT()),

            'get_samples_per_point' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_SAMPLES_PER_POINT()),

            'set_points_per_step' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_SET_POINTS_PER_STEP()),

            'get_points_per_step' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_POINTS_PER_STEP()),
            'cpy_FRAM_to_FPGA' : lambda: self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=get_FM_GET_CPY_SWT_FRAM_TO_FPGA())
        }
        self.fm_window = ButtonWindow("FM commands", get_fm_buttons(callbacks))
        self.fm_window.show()

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

                        # print(hex_str)
                        decoded = cobs.decode(buffer[:-1])
                        spp_header = SPP_decode(decoded[:6])

                        if(spp_header.sec_head_flag == 1):
                            pus_header = PUS_TM_decode(decoded[6:15])

                        hex_decoded = " ".join(f"0x{b:02X}" for b in decoded)
                        # print(hex_decoded)

                        if spp_header.packet_type == 0 and spp_header.sec_head_flag == 1:
                            if pus_header.service_id == 1:
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
                                if spp_header.packet_type == 0 and pus_header.service_id == 8 and pus_header.subtype_id == 1:
                                    self.uC_Sweep_Tables.Table[decoded[16]][decoded[17]] = decoded[18]<<8 | decoded[19]
                                item = QListWidgetItem(f"Received: {hex_str}")  # Create a list item
                                item.setForeground(QBrush(QColor("blue")))  # Set text color to blue
                            self.msg_list.addItem(item)

                        elif spp_header.packet_type == 0 and spp_header.sec_head_flag == 0:
                            print(hex_decoded)
                            item = QListWidgetItem(f"Received: {hex_str}")  # Create a list item
                            item.setForeground(QBrush(QColor("red")))  # Set text color to blue
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

                if pus_header.service_id == PUS_Service_ID.HOUSEKEEPING_SERVICE_ID.value and pus_header.subtype_id == PUS_HK_Subtype_ID.HK_PARAMETER_REPORT.value:
                    SID = (decoded[15] | (decoded[16] << 8))
                    if SID == 0xAAAA:
                        HK_report = HK_uC_Report()
                        HK_report.vbat_i = decoded[20] << 24 | decoded[19] << 16 | decoded[18] << 8 | decoded[17] 
                        HK_report.temperature_i = decoded[24] << 24 | decoded[23] << 16 | decoded[22] << 8 | decoded[21] 
                        HK_report.uc3v_i = decoded[28] << 24 | decoded[27] << 16 | decoded[26] << 8 | decoded[25] 
                        details.append("\nMicrocontroller Report Data:")
                        details.append(f"  VBAT_I: {HK_report.vbat_i}")
                        details.append(f"  TEMPERATURE_I: {HK_report.temperature_i}")
                        details.append(f"  UC3V_I: {HK_report.uc3v_i}")

                    if SID == 0x5555:
                        HK_report = HK_FPGA_Report()
                        HK_report.fpga1p5v_i = decoded[20] << 24 | decoded[19] << 16 | decoded[18] << 8 | decoded[17] 
                        HK_report.fpga3v_i = decoded[24] << 24 | decoded[23] << 16 | decoded[22] << 8 | decoded[21] 
                        details.append("\nFPGA Report Data:")
                        details.append(f"  FPGA_1P5V_I: {HK_report.fpga1p5v_i}")
                        details.append(f"  FPGA_3V_I: {HK_report.fpga3v_i}")
                
                elif pus_header.service_id == PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value and pus_header.subtype_id == PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value:
                    FM_SWT_report = FM_Sweep_Table_Report()
                    FM_SWT_report.target = decoded[15]
                    FM_SWT_report.sweep_table_id = decoded[16]
                    FM_SWT_report.step_id = decoded[17]
                    FM_SWT_report.voltage_level = decoded[18]<<8 | decoded[19] 
                    
                    details.append("\nSweep Table Info:")
                    details.append(f"  Target: {FM_SWT_report.target}")
                    details.append(f"  Sweep Table ID: {FM_SWT_report.sweep_table_id}")
                    details.append(f"  Step ID: {FM_SWT_report.step_id}")
                    details.append(f"  Voltage Level: {FM_SWT_report.voltage_level}")

            else:
                details.append("\nPUS Header: Not available or decode failed")

        elif spp_header.sec_head_flag == 0:

            if decoded[6] == Function_ID.GET_CB_VOL_LVL_ID.value:
                details.append("\nConstant Bias Info:")
                details.append(f"  Probe ID: {decoded[7]}")
                details.append(f"  Voltage Level: {decoded[8] << 8 | (decoded[9])}")
            elif decoded[6] == Function_ID.GET_SWT_VOL_LVL_ID.value:
                details.append("\nVoltage Level In Sweep Table:")
                details.append(f"  Table ID: {decoded[7]}")
                details.append(f"  Step ID: {decoded[8]}")
                details.append(f"  Voltage Level: {decoded[9] << 8 | (decoded[10])}")
            elif decoded[6] == Function_ID.GET_SWT_STEPS_ID.value:
                details.append("\nSweep Bias Mode info:")
                details.append(f"Nr of Steps: {decoded[7]}")
            elif decoded[6] == Function_ID.GET_SWT_SAMPLES_PER_STEP_ID.value:
                details.append("\nSweep Bias Mode info:")
                details.append(f"Nr of Samples per Step: {decoded[7] << 8 | decoded[8]}")
            elif decoded[6] == Function_ID.GET_SWT_SAMPLE_SKIP_ID.value:
                details.append("\nSweep Bias Mode info:")
                details.append(f"Nr of Skipped Samples: {decoded[7] << 8 | decoded[8]}")
            elif decoded[6] == Function_ID.GET_SWT_SAMPLES_PER_POINT_ID.value:
                details.append("\nSweep Bias Mode info:")
                details.append(f"Nr of Samples per Point: {decoded[7] << 8 | decoded[8]}")
            elif decoded[6] == Function_ID.GET_SWT_NPOINTS_ID.value:
                details.append("\nSweep Bias Mode info:")
                details.append(f"Nr of Samples per Point: {decoded[7] << 8 | decoded[8]}")
        
        self.details_edit.setText("\n".join(details))

    def clear_console(self):
        self.msg_list.clear()
        self.messages.clear()  # Also clear stored messages if needed

    def show_sw_table(self, index, category):
        if category == "mcu":
            plot_window = PlotWindow(self.uC_Sweep_Tables.Table[index], self)
            plot_window.exec_()
        elif category == "fpga":
            plot_window = PlotWindow(self.FPGA_Sweep_Tables.Table[index], self)
            plot_window.exec_()

    def set_sweep_table(self):
        table_index = 2
        table = Excel_table()
        for i in range(10):
            voltage_level = table.data_list[i]
            data = [Function_ID.SET_SWT_VOL_LVL_ID.value, 
                    0x04,   
                    Argument_ID.PROBE_ID_ARG_ID.value,     table_index,  
                    Argument_ID.STEP_ID_ARG_ID.value,      i,   
                    Argument_ID.VOL_LVL_ARG_ID.value,      voltage_level & 0xFF, (voltage_level >> 8) & 0xFF,
                    Argument_ID.GS_TARGET_ARG_ID.value,    0x01]
            
            print(table.data_list[i])
            print(voltage_level & 0xFF, (voltage_level >> 8) & 0xFF)
            self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=data)
            time.sleep(0.5)
            
    def get_sweep_table(self):
        table_index = 2
        for i in range(10):
            data = [Function_ID.GET_SWT_VOL_LVL_ID.value, 
                    0x03,   
                    Argument_ID.PROBE_ID_ARG_ID.value,     table_index,  
                    Argument_ID.STEP_ID_ARG_ID.value,      i,  
                    Argument_ID.GS_TARGET_ARG_ID.value,    0x01]
            
            self.send_command(service_id=PUS_Service_ID.FUNCTION_MANAGEMNET_ID.value,
                            sub_service_id=PUS_FM_Subtype_ID.FM_PERFORM_FUNCTION.value,
                            command_data=data)
            time.sleep(0.5)

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
    