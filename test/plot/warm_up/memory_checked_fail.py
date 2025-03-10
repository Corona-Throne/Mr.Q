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
    print(r"此劇情為模擬暖機 Memory Checked Fail 的情況，請將 <PLC memory address> 設置為 False")
    print()
    
    text = "Yes, please provide the warm-up preparation, and check the conditions."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()

    os.system("pause")

    text = "The status of air pressure has been checked, please provide the warm-up preparation again."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()

    text = "There is no balancing tool on the spindle. Where is the balance tool?"
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()

    text = "The balance tool has been manually installed, please check the warm-up condition again."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()