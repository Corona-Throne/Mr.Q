from PyQt5.QtCore import QTimer

from src.model.ui.speech_bubble.config import (
    MessageRole, MessageColor
)

class UserMessageSender:
    def __init__(self, parent, clear_seconds: float=0):
        self.parent = parent
        self.clear_seconds = clear_seconds
        self.message_timer = QTimer(self.parent)
        self.message_timer.timeout.connect(self._clear_edt)

    def send_message(self, message: str):
        self.message_timer.start(self.clear_seconds*1000)
        self.parent.send_message(
            MessageRole.USER, message.strip(), MessageColor.USER_DEFAULT
        )
    
    def _clear_edt(self):
        self.parent.ui.edt_voice_input.clear()