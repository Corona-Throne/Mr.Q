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
    print(r"此劇情為模擬暖機中，平衡刀正常放置的情況")
    print()
    
    text = "Yes, please provide the warm-up preparation, and check the conditions."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()

    text = "Yes, there is a balance tool on the spindle."
    print(f'{text}\n')
    messages = scenario.handle_message(text)
    for msg in messages['text']:
        print(f'>> {msg}')
        print()
