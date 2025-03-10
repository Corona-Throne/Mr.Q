import os
from dotenv import load_dotenv
load_dotenv()

from azure.cognitiveservices import speech

from src.model.stt.base import SpeechToText

class AzureSpeechToText(SpeechToText):

    def __init__(self) -> None:
        super().__init__()
        speech_config = speech.SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_KEY"), 
            region=os.getenv("AZURE_SPEECH_REGION")
        )
        speech_config.speech_recognition_language = "en-US"
        audio_config = speech.audio.AudioConfig(use_default_microphone=True)
        self.recognizer = speech.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )

    def recognize(self) -> str:
        """Recognize speech from user microphone.

        Note: The function recognize_once_async only records up to 30 seconds of speech.
        """
        result = self.recognizer.recognize_once_async().get()

        if result.reason == speech.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speech.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speech.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speech.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
        
        return ""