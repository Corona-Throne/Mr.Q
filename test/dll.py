import os
import clr
import sys
root_dir = os.getcwd()
clr.AddReference(os.path.join(root_dir, "dll/MrQ/MrQLib"))
sys.path.append(root_dir)

import MrQLib as Lib

class DLLTest:
    def __init__(self) -> None:
        self.conn = Lib.MachineConnection()
        self.conn.Connect("<mock dll library name>")

    def program_exist(self, name: str, root_dir: str) -> bool:
        pg = Lib.Program(name)
        pg.Find(self.conn, root_dir)
        return pg.Exist(self.conn)
    
    def program_download(self, name: str, root_dir: str, localfilepath: str):
        if os.path.isfile(localfilepath): os.remove(localfilepath)
        pg = Lib.Program(name)
        pg.Find(self.conn, root_dir)
        pg.Download(self.conn, localfilepath)

    def program_exectime(self, name: str, root_dir: str) -> float:
        pg = Lib.Program(name)
        pg.Find(self.conn, root_dir)
        return pg.GetExecTime()

    def carbon_emission_estimate(self, name: str, root_dir: str) -> float:
        pg = Lib.Program(name)
        pg.Find(self.conn, root_dir)
        emission_val = Lib.CarbonEmissionEstimator.Estimate(pg)
        return emission_val

    def memory_read(self, mem_path: str) -> str:
        return Lib.MemoryReader.Read(self.conn, mem_path)

    def get_programtool_name(self, name: str) -> str:
        tool = Lib.ProgramTool(name)
        return tool.GetToolName(self.conn)

    def get_programtool_number(self, name: str) -> str:
        tool = Lib.ProgramTool(name)
        return tool.GetToolNumber(self.conn)
    
    def check_programtool_val(self, name: str, tybe: str) -> str:
        tool = Lib.ProgramTool(name)
        return tool.CheckLR(self.conn, tybe)
    
    def automatic_event(self, dest_dir: str) -> None:
        events = Lib.AutomaticEvents(dest_dir)
        events.Init(self.conn)
    
    def program_search(self, name: str, root_dir) -> str:
        pg = Lib.Program(name)
        pg.Find(self.conn, root_dir)
        return pg.GetFilePath()
        

if __name__ == '__main__':
    mem_path = r"<mock memory address>"
    tool_number = "<mock tool number>"
    tool_name = "<mock tool name>"
    test = DLLTest()

    isexist = test.program_exist("mock program name", "PLC:\\plc\\")
    assert isexist == True

    filepath = test.program_search("O0002", "TNC:\\")
    assert filepath == r"TNC:\nc_prog\MR.Q\O0002.H"

    desfilepath = os.path.join(root_dir, r"test\tmp\O0002.H")
    test.program_download("O0002", "TNC:\\", desfilepath)
    assert os.path.isfile(desfilepath) == True

    exec_time = test.program_exectime("O0002", "TNC:\\")
    assert round(exec_time, 2) == round(5.4, 2)

    emission_val = test.carbon_emission_estimate("O0002", "TNC:\\")
    assert round(emission_val, 2) == round(exec_time*1.1, 2)

    val_str = test.memory_read(mem_path)
    assert val_str == "True"

    tool_name = test.get_programtool_name(tool_number)
    assert tool_name == tool_name

    tool_name = test.get_programtool_name(tool_name)
    assert tool_name == tool_name

    tool_number = test.get_programtool_number(tool_number)
    assert tool_number == tool_number

    tool_number = test.get_programtool_number(tool_name)
    assert tool_number == tool_number

    L_val = test.check_programtool_val(tool_number, "L")
    assert L_val == "120"

    R_val = test.check_programtool_val(tool_name, "R")
    assert R_val == "1"

    desfilepath = os.path.join(root_dir, r"test\tmp")
    test.automatic_event(desfilepath)

    os.system("pause")