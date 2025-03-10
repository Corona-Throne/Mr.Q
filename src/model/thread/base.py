from PyQt5.QtCore import QObject, QRunnable

class Worker(QObject):
    def do_task(self) -> None:
        """Don't forget override this function."""
        pass

class RunnableTask(QRunnable):
    def __init__(self, worker: QObject) -> None:
        super().__init__()
        self.setAutoDelete(True)
        self.worker = worker

    def run(self) -> None:
        self.worker.do_task()