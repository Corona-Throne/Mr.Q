import abc

class PromptTemplate(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def format(*args) -> str:
        pass