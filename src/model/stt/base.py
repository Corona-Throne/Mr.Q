import abc

from PyQt5.QtCore import pyqtSignal

from src.model.thread.base import Worker

class SpeechToText(abc.ABC):
    @abc.abstractmethod
    def recognize(self) -> str:
        pass

class SpeechToTextWorker(Worker):
    result_ready = pyqtSignal(str)

    def __init__(self, stt: SpeechToText):
        super().__init__()
        self.stt = stt

    def do_task(self):
        result = self.stt.recognize()
        self.result_ready.emit(result)
