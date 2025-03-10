import os
import sys
import clr
from dotenv import load_dotenv
clr.AddReference(os.path.join(os.getcwd(), "dll/MrQ/MrQLib"))
sys.path.append(os.getcwd())
load_dotenv()

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QThreadPool, QCoreApplication

import MrQLib as Lib
from src.ui import MrQ_UI
from src.model.stt.base import SpeechToTextWorker
from src.model.thread.base import RunnableTask
from src.model.stt.azure import AzureSpeechToText
from src.model.tts.azure import AzureTextToSpeech
from src.model.ui.gif.player import GifPlayer
from src.model.ui.speech_bubble.listview_model import MessageModel
from src.model.ui.speech_bubble.message_style import MessageDelegate
from src.model.ui.speech_bubble.config import MessageRole, MessageColor
from src.model.scenario.handler.base import MessageHandlerWorker
from src.model.scenario.handler.mrq import MrQHandler
from src.model.ui.message_sender.ai import AIMessageSender
from src.model.ui.message_sender.user import UserMessageSender
from src.model.ui.carbon_footprint.timer import CarbonFootprintTimer


class MrQ_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MrQ_UI()
        self.ui.setup_ui(self)
        self.init_module()
        self.setup_control()

    def init_module(self):
        conn = Lib.MachineConnection()
        conn.Connect(os.getenv("TNC_NAME")) # connect to CNC
        self._translate = QCoreApplication.translate
        self.threadpool = QThreadPool.globalInstance()
        self.stt = AzureSpeechToText()
        self.tts = AzureTextToSpeech()
        self.wave_player = GifPlayer(widget=self.ui.lb_audio_wave)
        self.lv_model = MessageModel()
        self.scenario = MrQHandler(conn, self.send_message)
        self.ai_message_sender = AIMessageSender(self, delay_seconds=1.0)
        self.user_message_sender = UserMessageSender(self, clear_seconds=2.0)
        self.carbon_footprint_timer = CarbonFootprintTimer(self, conn, interval_seconds=8)

    def setup_control(self):
        self.ui.btn_microphone.clicked.connect(self.btn_clicked_event)
        self.ui.lv_messages.setItemDelegate(MessageDelegate())
        self.ui.lv_messages.setModel(self.lv_model)
        self.ui.edt_voice_input.textChanged.connect(self.edt_textchanged_event)
        self._init_ai_messages()
        
    def btn_clicked_event(self):
        self.ui.btn_microphone.setEnabled(False)
        self.ui.edt_voice_input.clear()
        # start animation of audio wave gif when microphone starts recording
        self.wave_player.play()
        # start speech-to-text service
        worker = SpeechToTextWorker(self.stt)
        worker.result_ready.connect(self._stt_result_handling)
        task = RunnableTask(worker=worker)
        self.threadpool.start(task)
    
    def _stt_result_handling(self, result: str):
        self.wave_player.stop()
        self.ui.btn_microphone.setEnabled(True)
        if len(result) == 0: return
        # set result to edt_voice_input QLineEdit object if result has value
        self.ui.edt_voice_input.setText(self._translate("MainWindow", result))

    def edt_textchanged_event(self, text: str):
        if len(text) == 0: return
        self.user_message_sender.send_message(text)
        self._ai_response(text)

    def _init_ai_messages(self):
        worker = MessageHandlerWorker(self.scenario)
        worker.result_ready.connect(self.ai_message_sender.send_message)
        task = RunnableTask(worker=worker)
        self.threadpool.start(task)

    def _ai_response(self, user_text: str):
        worker = MessageHandlerWorker(self.scenario, user_text)
        worker.result_ready.connect(self.ai_message_sender.send_message)
        task = RunnableTask(worker=worker)
        self.threadpool.start(task)

    def send_message(self, role: MessageRole, message: str, color: MessageColor):
        self.lv_model.add_message(role, message, color)
        self.ui.lv_messages.scrollToBottom()
        QApplication.processEvents()
        # text to speech
        if role == MessageRole.AI:
            self.tts.speak(message.split('\n')[0])

    def set_carbon_footprint(self, n_kg: float):
        self.ui.lb_kg.setText(self._translate("MainWindow", f'CO2\n{n_kg:.3f} kg'))