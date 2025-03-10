from typing import List, Callable

from PyQt5.QtCore import pyqtSignal

from src.model.dnc.valid.valider import Valider
from src.model.scenario.timer.base import UntilCompletedWorker
from src.model.ui.speech_bubble.config import MessageRole, MessageColor

class WarmUpWorker(UntilCompletedWorker):
    _updated = pyqtSignal(int, str, str)

    def __init__(self, conn, m_paths: List[str], stds: List[str], callback: Callable) -> UntilCompletedWorker:
        super().__init__()
        self._conn = conn
        self._memory_paths: List[str] = m_paths
        self._standards: List[str] = stds
        self._updated.connect(callback)

    def _task(self) -> bool:
        if Valider.valid_multi_values(self._conn, self._memory_paths, self._standards):
            self._updated.emit(MessageRole.AI, "Warm-up completed.", MessageColor.AI_DEFAULT)
            self._is_finished = True