import os
import MrQLib as Lib
from dotenv import load_dotenv
load_dotenv()

from PyQt5.QtCore import QTimer

class CarbonFootprintTimer:
    def __init__(self, parent, conn: Lib.MachineConnection, interval_seconds: float=0):
        self.parent = parent
        self.conn = conn
        self.last_val = 0
        self.timer = QTimer(self.parent)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(interval_seconds*1000)

    def update_value(self) -> None:
        try:
            val_str = Lib.MemoryReader.Read(self.conn, os.getenv("CARBON_FOOTPRINT_PATH"))
            val_f = float(val_str) / 1000
            self.parent.set_carbon_footprint(val_f)
            self.last_val = val_f
        except:
            self.parent.set_carbon_footprint(self.last_val)
