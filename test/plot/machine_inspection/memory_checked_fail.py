import os
import sys
import clr
from dotenv import load_dotenv
clr.AddReference(os.path.join(os.getcwd(), "dll/MrQ/MrQLib"))
sys.path.append(os.getcwd())
load_dotenv()

from src.model.scenario.handler.mrq import MrQHandler

import MrQLib as Lib
conn = Lib.MachineConnection()
conn.Connect(os.getenv("TNC_NAME")) # connect to CNC

def mock_send_message(self, role, message, color):
    pass

scenario = MrQHandler(conn, mock_send_message)

if __name__ == "__main__":
    print()
    print(r"此劇情為模擬機器檢查 Memory Checked Fail 的情況，請將 \PLC\memory\I\263 設置為 False")
    print()
    
    text = "Please check the machine conditions."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()

    text = "Please download program O0002"
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()

    os.system("pause")

    text = "The status of axial lubricant supply has been checked, please check the machine conditions again."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()

    text = "The cutting coolant has been refilled."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()