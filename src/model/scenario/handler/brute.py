
from src.model.scenario.handler.base import Handler
from src.model.utile.file import load_json

class BruteHandler(Handler):
    
    def load_ai_script(self, script: str):
        self.index = 0
        script = load_json(script)
        self.ai_messages = list(script.values())
    
    def init_message(self):
        messages = self.ai_messages[self.index]
        self.__plus_index()
        return messages

    def handle_message(self, message: str):
        ai_response = self.ai_messages[self.index]
        self.__plus_index()
        return ai_response

    def __plus_index(self):
        if self.index >= len(self.ai_messages)-1: return
        self.index += 1