import abc
from typing import Dict, Any

class StructureChecker(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def check(obj: Dict[str, Any]) -> None:
        pass