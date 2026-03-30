import sys
import os
import datetime
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

class Sweep_Tables:
    def __init__(self):
        self.Table = [[0] * 256 for _ in range(11)]

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

class MacroSweepCollector: # collects Macro Sweep Bias TM packets by subop and saves them to Excel
    # metadata structure in TM 
    META_FIELDS = [("nof_act_sw_last_power_off", 11, 2),
                   ("nof_steps_sb_mode",         13, 1),
                   ("nof_samples_per_step",      14, 2),
                   ("nof_skipped_samples",       16, 2),
                   ("nof_samples_per_point",     18, 2),
                   ("nof_points_per_step",       20, 2),]
    # expecting conditions for each subop
    READY_RULES = {0x01: ("meta",),
                   0x02: ("nstep",),
                   0x03: ("full",),
                   0x04: ("meta", "nstep"),
                   0x05: ("meta", "full"),}

    def __init__(self):
        self.reset()

    def reset(self):
        self.metadata_by_subop = {}
        self.tables_by_subop = {}
        self.saved_once = set()

    def _initialize_subop_storage(self, subop):             # creates empty storage for a subop
        self.metadata_by_subop.setdefault(
            subop,
            {name: None for name, _, _ in self.META_FIELDS} )
        self.tables_by_subop.setdefault(
            subop,
            {   "nstep": {"total_steps_raw": None, "rows": {}},
                "full":  {"total_steps_raw": None, "rows": {}}, } )

    def process_macro_tm_packets(self, decoded):            # entry point for TM packets
        if decoded is None or len(decoded) < 11:
            return

        subop, packet_type, total_steps_raw, start_step = decoded[7:11]
        payload = decoded[11:]
        self._initialize_subop_storage(subop)

        if packet_type == 0x00:
            self._decode_metadata_packet(subop, decoded)
        elif packet_type == 0x01:
            self._decode_table_packet(subop, "nstep", total_steps_raw, start_step, payload)
        elif packet_type == 0x02:
            self._decode_table_packet(subop, "full", total_steps_raw, start_step, payload)

    def _read_uint16_be(self, data, idx):                   # big-endian
        return (data[idx] << 8) | data[idx + 1]

    def _decode_metadata_packet(self, subop, decoded):      # decode and store metadata
        if len(decoded) < 22:
            return

        meta = {}
        for name, idx, size in self.META_FIELDS:
            meta[name] = decoded[idx] if size == 1 else self._read_uint16_be(decoded, idx)
        self.metadata_by_subop[subop] = meta

    def _decode_table_packet(self, subop, table_kind, total_steps_raw, start_step, payload): # decode and store tables
        store = self.tables_by_subop[subop][table_kind]
        store["total_steps_raw"] = total_steps_raw
        store["last_payload_hex"] = " ".join(f"{b:02X}" for b in payload)

        for i in range(len(payload) // 4):
            base = i * 4
            store["rows"][start_step + i] = {
                "table0": self._read_uint16_be(payload, base),
                "table1": self._read_uint16_be(payload, base + 2), }

    def _metadata_received(self, subop):
        return any(v is not None for v in self.metadata_by_subop.get(subop, {}).values())

    def _table_received(self, subop, table_kind):            
        store = self.tables_by_subop[subop][table_kind]
        total = store["total_steps_raw"]
        return total is not None and len(store["rows"]) >= total + 1

    def ready_2_save(self, subop):                          # checks required data for subop
        self._initialize_subop_storage(subop)

        status = {"meta": self._metadata_received(subop),
                "nstep": self._table_received(subop, "nstep"),
                "full": self._table_received(subop, "full"), }

        needed = self.READY_RULES.get(subop, ())
        return all(status[key] for key in needed)

    def _build_table_dataframe(self, subop, table_kind):    # build dataframe for collected tables
        rows = self.tables_by_subop[subop][table_kind]["rows"]
        if not rows:
            return pd.DataFrame(columns=["Step", "Table 0", "Table 1"])

        steps = sorted(rows)
        return pd.DataFrame({"Step": steps,
                            "Table 0": [rows[s]["table0"] for s in steps],
                            "Table 1": [rows[s]["table1"] for s in steps], })

    def save_macro_data(self, subop, base_dir="."):         # save in workbook 
        if subop in self.saved_once:
            return []

        self._initialize_subop_storage(subop)
        if not self.ready_2_save(subop):
            return []

        file_path = os.path.join(base_dir, "Macro_Sweep_Bias.xlsx")
        meta = self.metadata_by_subop[subop]
        tables = self.tables_by_subop[subop]
        
        # metadata sheet row wise
        meta_rows = [["subop", f"0x{subop:02X}"]]
        meta_rows += [["nstep_total_steps", tables["nstep"]["total_steps_raw"]],
                    ["full_total_steps", tables["full"]["total_steps_raw"]], ]
        meta_rows += [[name, meta[name]] for name, _, _ in self.META_FIELDS]
        meta_df = pd.DataFrame(meta_rows, columns=["Field", "Value"])   
        
        # write all sheets
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            meta_df.to_excel(writer, sheet_name="Metadata", index=False)
            self._build_table_dataframe(subop, "nstep").to_excel(writer, sheet_name="N_Steps_Table", index=False)
            self._build_table_dataframe(subop, "full").to_excel(writer, sheet_name="Full_Table", index=False)

        self.saved_once.add(subop)
        return [file_path]
    
if __name__ == "__main__":
    table = Excel_table()

