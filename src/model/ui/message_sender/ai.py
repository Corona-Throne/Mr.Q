from typing import Dict, List

from PyQt5.QtCore import QTimer
from PyQt5 import QtMultimedia

from src.model.ui.speech_bubble.config import (
    MessageRole, MessageColor, ScriptMessageColor
)

class AIMessageSender:
    def __init__(self, parent, delay_seconds: float=0):
        self.parent = parent
        self.delay_seconds = delay_seconds
        self.ai_message_queue = None
        self.message_index = 0
        self.message_timer = QTimer(self.parent)
        self.message_timer.timeout.connect(self._send_next_message)

    def send_message(self, messages: Dict[str, List[str]]):
        self.ai_message_queue = messages
        self.message_index = 0
        self.message_timer.start(self.delay_seconds*1000)

    def _send_next_message(self):
        if self.message_index < len(self.ai_message_queue['text']):
            message = self.ai_message_queue['text'][self.message_index].strip()
            color = self.ai_message_queue['color'][self.message_index]

            if color == ScriptMessageColor.DEFAULT:
                color = MessageColor.AI_DEFAULT
            elif color == ScriptMessageColor.WARNING:
                color = MessageColor.AI_WARNING
            else:
                color = MessageColor.AI_MURMUR

            self.parent.send_message(MessageRole.AI, message, color)

            self.message_index += 1
        else:
            self.message_timer.stop()
            QtMultimedia.QSound.play('src\\audio\\hint.wav')