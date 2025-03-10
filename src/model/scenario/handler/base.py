import abc
from typing import Optional

from PyQt5.QtCore import pyqtSignal

from src.model.thread.base import Worker

class Handler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def init_message(self):
        pass
    
    @abc.abstractmethod
    def handle_message(self, message: str):
        pass

class MessageHandlerWorker(Worker):
    result_ready = pyqtSignal(object)

    def __init__(self, handler: Handler, message: Optional[str]=""):
        super().__init__()
        self.handler = handler
        self.message = message

    def do_task(self):
        if self.message:
            result = self.handler.handle_message(self.message)
        else: 
            result = self.handler.init_message()
            
        if len(result['text']) == 0: return # check result is not empty.
        self.result_ready.emit(result)