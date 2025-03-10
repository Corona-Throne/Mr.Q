import abc

from src.model.thread.base import Worker

class TextToSpeech(abc.ABC):
    @abc.abstractmethod
    def speak(self, text: str) -> None:
        pass

class TextToSpeechWorker(Worker):

    def __init__(self, tts: TextToSpeech, text: str):
        super().__init__()
        self.tts = tts
        self.text = text

    def do_task(self):
        self.tts.speak(self.text)
