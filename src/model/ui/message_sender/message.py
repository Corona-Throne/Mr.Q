from typing import Dict, List, Optional

from src.model.ui.speech_bubble.config import MessageColor

class ColorMessage:
    def __init__(self) -> None:
        self._color: List = []
        self._messages: List = []

    def add_message(
        self, msg: str, color: Optional[MessageColor]=MessageColor.AI_DEFAULT
    ) -> None:
        self._messages.append(msg.strip())
        self._color.append(color)
    
    def remove_last_message(self) -> None:
        if len(self._messages) > 0:
            del self._messages[-1]
        if len(self._color) > 0:
            del self._color[-1]

    def get_dict(self) -> Dict[str, List[str]]:
        return {
            "text": self._messages,
            "color": self._color
        }