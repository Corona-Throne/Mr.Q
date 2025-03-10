import abc
from PyQt5.QtCore import pyqtSignal, QThread

from src.model.thread.base import Worker

class UntilCompletedWorker(Worker):
    finished = pyqtSignal()

    def __init__(self) -> "UntilCompletedWorker":
        super().__init__()
        self._is_finished = False
    
    @abc.abstractmethod
    def _task(self) -> bool:
        pass

    def do_task(self) -> None:
        while not self._is_finished:
            self._task()
            QThread.msleep(1000)  # Simulate work being done
        self.finished.emit()