from typing import Dict, Any

from src.model.scenario.script.base import StructureChecker
from src.model.utile.error import *

class BaseStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "action_type" not in obj: raise AttributeNotFoundError("action_type")

class EchoStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "text" not in obj: raise AttributeNotFoundError("text")

class EchoThenWaitStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "text" not in obj: raise AttributeNotFoundError("text")

class EchoMemoryStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "text" not in obj: raise AttributeNotFoundError("text")
        if "params" not in obj: raise AttributeNotFoundError("params")
        if "path" not in obj['params']: raise AttributeNotFoundError("path")
        if "process" not in obj['params']: raise AttributeNotFoundError("path")

class ReadMemoryStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "params" not in obj: raise AttributeNotFoundError("params")
        if "response" not in obj: raise AttributeNotFoundError("response")
        if "path" not in obj['params']: raise AttributeNotFoundError("path")
        if "standard" not in obj['params']: raise AttributeNotFoundError("standard")
        if "ok" not in obj['response']: raise AttributeNotFoundError("ok")
        if "error" not in obj['response']: raise AttributeNotFoundError("error")

class CheckEnvStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "field" not in obj: raise AttributeNotFoundError("field")
        if "standard" not in obj: raise AttributeNotFoundError("standard")

class SetEnvStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "key" not in obj: raise AttributeNotFoundError("key")
        if "value" not in obj: raise AttributeNotFoundError("value")

class UpdateEnvStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "key" not in obj: raise AttributeNotFoundError("key")
        if "cmd" not in obj: raise AttributeNotFoundError("cmd")

class AnswerMsgStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "prompt_type" not in obj: raise AttributeNotFoundError("prompt_type")
        if "prompt" not in obj: raise AttributeNotFoundError("prompt")
        if "is_finished" not in obj: raise AttributeNotFoundError("is_finished")

class CheckKeywordStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "keyword" not in obj: raise AttributeNotFoundError("keyword")
        if "ok" not in obj: raise AttributeNotFoundError("ok")
        if "error" not in obj: raise AttributeNotFoundError("error")

class ExistProgramStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "program" not in obj: raise AttributeNotFoundError("program")
        if "response" not in obj: raise AttributeNotFoundError("response")
        if "name" not in obj['program']: raise AttributeNotFoundError("name")
        if "root" not in obj['program']: raise AttributeNotFoundError("root")
        if "ok" not in obj['response']: raise AttributeNotFoundError("ok")
        if "error" not in obj['response']: raise AttributeNotFoundError("error")

class UntilCompletedStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "task_type" not in obj: raise AttributeNotFoundError("task_type")

class WarmUpStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "params" not in obj: raise AttributeNotFoundError("params")
        if "path" not in obj['params']: raise AttributeNotFoundError("path")
        if "standard" not in obj['params']: raise AttributeNotFoundError("standard")

class LoopEventStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "events" not in obj: raise AttributeNotFoundError("events")
        if "finish" not in obj: raise AttributeNotFoundError("finish")

class JumpToStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "step" not in obj: raise AttributeNotFoundError("step")

class ProgramExecutionRecordStructureChecker(StructureChecker):

    @staticmethod
    def check(obj: Dict[str, Any]) -> None:
        if "response" not in obj: raise AttributeNotFoundError("response")
        if "ok" not in obj['response']: raise AttributeNotFoundError("ok")
        if "error" not in obj['response']: raise AttributeNotFoundError("error")