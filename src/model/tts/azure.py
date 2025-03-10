import os
from dotenv import load_dotenv
load_dotenv()

from azure.cognitiveservices import speech

from src.model.tts.base import TextToSpeech

class AzureTextToSpeech(TextToSpeech):

    def __init__(self) -> None:
        super().__init__()
        speech_config = speech.SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_KEY"), 
            region=os.getenv("AZURE_SPEECH_REGION")
        )
        # JasonNeural
        speech_config.speech_synthesis_voice_name='en-US-JasonNeural'
        audio_config = speech.audio.AudioOutputConfig(use_default_speaker=True)
        self.speaker = speech.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    def speak(self, text: str) -> None:
        """Recognize speech from user microphone.

        Note: The function recognize_once_async only records up to 30 seconds of speech.
        """
        result = self.speaker.speak_text_async(text).get()

        if result.reason == speech.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif result.reason == speech.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speech.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")