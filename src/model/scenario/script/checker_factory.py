from typing import Dict, Any

from src.model.scenario.script.checker import *
from src.model.utile.error import *

class StructureCheckerFactory:

    @staticmethod
    def check(tybe: str, obj: Dict[str, Any]) -> None:
        if type == "base":
            BaseStructureChecker.check(obj)
        elif tybe == "echo":
            EchoStructureChecker.check(obj)
        elif tybe == "echo_then_wait":
            EchoThenWaitStructureChecker.check(obj)
        elif tybe == "echo_memory":
            EchoMemoryStructureChecker.check(obj)
        elif tybe == "read_memory":
            ReadMemoryStructureChecker.check(obj)
        elif tybe == "check_var" or tybe == "check_global":
            CheckEnvStructureChecker.check(obj)
        elif tybe == "set_var" or tybe == "set_global":
            SetEnvStructureChecker.check(obj)
        elif tybe == "update_var":
            UpdateEnvStructureChecker.check(obj)
        elif tybe == "estimate_carbon_emission":
            EchoStructureChecker.check(obj) # 暫時...
        elif tybe == "answer_msg":
            AnswerMsgStructureChecker.check(obj)
        elif tybe == "check_keyword":
            CheckKeywordStructureChecker.check(obj)
        elif tybe == "exist_program":
            ExistProgramStructureChecker.check(obj)
        elif tybe == "until_completed":
            UntilCompletedStructureChecker.check(obj)
        elif tybe == "warmup":
            WarmUpStructureChecker.check(obj)
        elif tybe == "loop_events":
            LoopEventStructureChecker.check(obj)
        elif tybe == "jump_to":
            JumpToStructureChecker.check(obj)
        elif tybe == "check_program_execution_record":
            ProgramExecutionRecordStructureChecker.check(obj)