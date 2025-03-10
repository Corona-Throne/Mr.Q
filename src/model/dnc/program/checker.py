import os
import re
import MrQLib as Lib
from typing import List
from dotenv import load_dotenv
load_dotenv()

from src.model.utile.file import load_txt

class ProgramToolChecker:

    @staticmethod
    def check(conn: Lib.MachineConnection, pg: Lib.Program) -> List[str]:
        filepath = os.path.join(os.getcwd(), os.getenv("PROGRAM_PATH"), pg.GetFileName())
        if not os.path.isfile(filepath): return list()
        content = load_txt(filepath)
        lines = content.strip().split('\n')
        filtered_lines = list(filter(lambda x: "TOOL CALL" in x, lines))
        tool_names = list(map(
            lambda x: re.search(r'TOOL CALL\s+"?([^"\s]+)"?\s*', x).group(1), 
            filtered_lines
        ))
        
        missing_tools = []
        for name in tool_names:
            if ProgramToolChecker._check_if_tool_number(name):
                name = f'T{int(name)}'

            tool = Lib.ProgramTool(name)
            L_val = tool.CheckLR(conn, "L")
            R_val = tool.CheckLR(conn, "R")
            if L_val and R_val and eval(f'{L_val} > 0 and {R_val} > 0'):
                continue
            missing_tools.append(tool.GetToolNumber(conn))
        return missing_tools
    
    @staticmethod
    def _check_if_tool_number(name: str) -> bool:
        try:
            int(name)
            return True
        except Exception:
            return False