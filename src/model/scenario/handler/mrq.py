import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Callable
from datetime import datetime, timedelta
load_dotenv()

import MrQLib as Lib
from PyQt5.QtCore import QThread

from src.model.utile.error import *
from src.model.chat.azure import GPT35
from src.model.utile.file import load_json
from src.model.dnc.valid.valider import Valider
from src.model.scenario.handler.base import Handler
from src.model.dnc.record.reader import RecordReader
from src.model.scenario.timer.warmup import WarmUpWorker
from src.model.scenario.env.enviroment import Enviroment
from src.model.ui.speech_bubble.config import MessageColor
from src.model.dnc.program.checker import ProgramToolChecker
from src.model.ui.message_sender.message import ColorMessage
from src.model.prompt.template_factory import PromptTemplateFactory
from src.model.scenario.script.checker_factory import StructureCheckerFactory

class MrQHandler(Handler):
    def __init__(self, conn: Lib.MachineConnection, callback: Callable) -> None:
        super().__init__()
        self._callback = callback # send message function

        self._env = Enviroment()
        self.conn = conn
        # init events saver
        event_storage_path = os.path.join(os.getcwd(), os.getenv("EVENT_PATH"))
        events = Lib.AutomaticEvents(event_storage_path)
        events.Init(self.conn)
        # init gpt
        self._gpt = GPT35(temperature=0.7)

    def init_message(self) -> Dict[str, List[str]]:
        script = self._load_script("init")
        messages = ColorMessage()
        '''add init message from the script'''
        if "messages" in script:
            for item in script["messages"]:
                messages.add_message(item)
        '''last shutdown time'''
        last_shutdown_time = datetime.now()-timedelta(days=1)
        last_shutdown_time_str = last_shutdown_time.strftime("%d/%m/%Y %H:%M")
        messages.add_message("Last shutdown time: {0}".format(last_shutdown_time_str))
        '''ask whether to start the warm-up process'''
        messages.add_message("Do you need to start warming up the machine?")
        return messages.get_dict()

    def handle_message(self, user_message: str) -> Dict[str, List[str]]:
        messages = ColorMessage()
        user_message = user_message.lower()
        self._env.wait_for_user_reply = False
        is_end = False

        if "exit" in user_message.strip() and self._env.state:
            '''使用者期望離開當下的作業流程'''
            self._exit_script(save=False)
            messages.add_message("Roger that.")
            return messages.get_dict()

        while not self._env.wait_for_user_reply:
            if is_end: 
                self._exit_script(save=False)
                break
            if self._env.state:
                '''使用者根據作業流程回覆'''
                cur_operation = self._env.get_cur_operation()
                if not cur_operation: raise WorkNotFoundError(self._env.step)
                StructureCheckerFactory.check("base", cur_operation)
                StructureCheckerFactory.check(cur_operation['action_type'], cur_operation)
                if cur_operation['action_type'] == "echo":
                    self._env.set_action(cur_operation['action_type'])
                    messages.add_message(cur_operation['text'])
                elif cur_operation['action_type'] == "echo_then_wait":
                    self._env.set_action("echo")
                    self._env.set_action("wait_for_user_reply")
                    messages.add_message(cur_operation['text'])
                    self._env.wait_for_user_reply = True
                elif cur_operation['action_type'] == "echo_memory":
                    self._env.set_action(cur_operation['action_type'])
                    if len(cur_operation['params']['path']) != len(cur_operation['params']['process']):
                        print("Path and process have different lengths in params.")
                        continue
                    params = []
                    for m,p in zip(cur_operation['params']['path'], cur_operation['params']['process']):
                        val_str = Lib.MemoryReader.Read(self.conn, m)
                        val_f = eval("{0} {1}".format(val_str, p))
                        params.append(val_f)
                    text = cur_operation['text'].format(*params)
                    messages.add_message(text)
                elif cur_operation['action_type'] == "exist_program":
                    self._env.set_action(cur_operation['action_type'])
                    pg_name = cur_operation['program']['name']
                    search_dir = cur_operation['program']['root']
                    pg = Lib.Program(pg_name)
                    pg.Find(self.conn, search_dir)
                    resp_ok = cur_operation['response']['ok']
                    resp_err = cur_operation['response']['error']
                    if pg.Exist(self.conn):
                        StructureCheckerFactory.check("base", resp_ok)
                        if resp_ok['action_type'] == "echo":
                            self._env.set_action(resp_ok['action_type'])
                            StructureCheckerFactory.check(resp_ok['action_type'], resp_ok)
                            text = resp_ok['text'].format(pg.Name)
                            messages.add_message(text)
                    else:
                        for action in resp_err:
                            self._env.set_action(action['action_type'])
                            StructureCheckerFactory.check("base", action)
                            StructureCheckerFactory.check(action['action_type'], action)
                            if action['action_type'] == "echo":
                                text = action['text'].format(pg.Name)
                                messages.add_message(text, MessageColor.AI_WARNING)
                            elif action['action_type'] == "exit":
                                self._exit_script(save=False)
                                return messages.get_dict()
                elif cur_operation['action_type'] == "download_program":
                    if self._env.get_last_action() != "wait_for_user_reply":
                        messages.add_message("What is the name of the program you want to download?")
                        self._env.set_action("wait_for_user_reply")
                        return messages.get_dict()
                    self._env.set_action(cur_operation['action_type'])
                    # Get the name of program
                    prompt = PromptTemplateFactory.format(
                        cur_operation['program']['prompt_type'], cur_operation['program']['prompt'], user_message
                    )
                    (is_ok, result) = self._gpt.completion(prompt)
                    if not is_ok:
                        text = (result + " Please say it again.").strip()
                        messages.add_message(text, MessageColor.AI_WARNING)
                        self._env.set_action("wait_for_user_reply")
                        return messages.get_dict()
                    pg_name = result
                    pg_root = cur_operation['program']['root']
                    pg = Lib.Program(pg_name)
                    pg.Find(self.conn, pg_root)
                    self._env.set_variable("program_name", pg_name)
                    self._env.set_variable("program_root", pg_root)
                    if not pg.GetFilePath(): 
                        messages.add_message("The program does not exist, please download program O0002 or O0003.", MessageColor.AI_WARNING)
                        self._env.set_action("wait_for_user_reply")
                        return messages.get_dict()
                    local_filepath = os.path.join(os.getcwd(), os.getenv("PROGRAM_PATH"), pg.GetFileName())
                    if os.path.isfile(local_filepath): os.remove(local_filepath)
                    pg.Download(self.conn, local_filepath)
                    if os.path.isfile(local_filepath):
                        self._env.set_variable("program_local_path", local_filepath)
                        messages.add_message("Program has been downloaded.")
                    else:
                        messages.add_message("Download program failed, please contact the staff.", MessageColor.AI_WARNING)
                        self._env.set_action("wait_for_user_reply")
                        return messages.get_dict()
                elif cur_operation['action_type'] == "read_memory":
                    self._env.set_action(cur_operation['action_type'])
                    memory_paths = cur_operation['params']['path']
                    standards = cur_operation['params']['standard']
                    result = Valider.valid_multi_values(self.conn, memory_paths, standards)
                    resp_ok = cur_operation['response']['ok']
                    resp_err = cur_operation['response']['error']
                    if result:
                        StructureCheckerFactory.check("base", resp_ok)
                        if resp_ok['action_type'] == "echo":
                            self._env.set_action(resp_ok['action_type'])
                            StructureCheckerFactory.check(resp_ok['action_type'], resp_ok)
                            messages.add_message(resp_ok['text'])
                    else:
                        for action in resp_err:
                            self._env.set_action(action['action_type'])
                            StructureCheckerFactory.check("base", action)
                            StructureCheckerFactory.check(action['action_type'], action)
                            if action['action_type'] == "echo":
                                messages.add_message(action['text'], MessageColor.AI_WARNING)
                            elif action['action_type'] == "echo_memory":
                                if len(action['params']['path']) != len(action['params']['process']):
                                    print("Path and process have different lengths in params.")
                                    continue
                                params = []
                                for m,p in zip(action['params']['path'], action['params']['process']):
                                    val_str = Lib.MemoryReader.Read(self.conn, m)
                                    val_f = eval("{0} {1}".format(val_str, p))
                                    params.append(val_f)
                                text = action['text'].format(*params)
                                messages.add_message(text, MessageColor.AI_WARNING)
                            elif action['action_type'] == "check_global":
                                val = self._env.get_global_var(action['field'])
                                result = eval("{0} {1}".format(val, action['standard'])) if val else True
                                if not result: break # True: 繼續之後的行動，False: 中斷之後的行動
                            elif action['action_type'] == "wait_for_user_reply":
                                self._env.wait_for_user_reply = True
                                break
                            elif action['action_type'] == "exit":
                                self._exit_script(save=False)
                                return messages.get_dict()
                elif cur_operation['action_type'] == "answer_msg":
                    if self._env.get_last_action() != "wait_for_user_reply":
                        is_end = self._env.next_step()
                        continue
                    self._env.set_action(cur_operation['action_type'])
                    prompt = PromptTemplateFactory.format(cur_operation['prompt_type'], cur_operation['prompt'], user_message)
                    (is_ok, result) = self._gpt.completion(prompt)
                    if not is_ok:
                        self._env.wait_for_user_reply = True
                        text = (result + " Please say it again.").strip()
                        messages.add_message(text, MessageColor.AI_WARNING)
                        return messages.get_dict()
                    messages.add_message(result)
                    is_finished = cur_operation['is_finished']
                    StructureCheckerFactory.check("base", is_finished)
                    StructureCheckerFactory.check(is_finished['action_type'], is_finished)
                    if is_finished['action_type'] == "check_keyword":
                        self._env.set_action(is_finished['action_type'])
                        resp_ok = is_finished['ok']
                        resp_err = is_finished['error']
                        is_continue = False
                        if is_finished['keyword'] in result:
                            '''response ok'''
                            if isinstance(resp_ok, dict):
                                resp_ok = [resp_ok]
                                
                            for action in resp_ok:
                                self._env.set_action(action['action_type'])
                                StructureCheckerFactory.check("base", action)
                                StructureCheckerFactory.check(action['action_type'], action)
                                if action['action_type'] == "echo":
                                    text = action['text']
                                    if "format" in action and action['format']:
                                        items = [self._env.get_variable(k) for k in action['format']]
                                        text = action['text'].format(*items)
                                    messages.add_message(text)
                                elif action['action_type'] == "set_global":
                                    self._env.set_global_var(action['key'], action['value'])
                                elif action['action_type'] == "update_var":
                                    var = self._env.get_variable(action['key'])
                                    splited_cmd = action['cmd'].split()
                                    if splited_cmd[0] == "remove":
                                        if splited_cmd[1] == "index":
                                            index = eval(splited_cmd[2])
                                            del var[index]
                                elif action['action_type'] == "jump_to":
                                    self._env.step = action['step']
                                    is_continue = True
                                    break
                        elif "alarm list" in result:
                            self._env.set_action('wait_for_user_reply')
                            messages.remove_last_message()
                            tool_number = self._env.get_variable("tool_number")
                            latest_time = RecordReader.readToolChange(tool_number)
                            if latest_time:
                                msg = RecordReader.readErrorMessage(latest_time)
                                if msg: messages.add_message(msg)
                            else:
                                text = "There is no tool change record related to {0}".format(tool_number)
                                messages.add_message(text)
                            self._env.wait_for_user_reply = True
                            return messages.get_dict()
                        else:
                            '''response error'''
                            self._env.set_action(resp_err['action_type'])
                            StructureCheckerFactory.check("base", resp_err)
                            StructureCheckerFactory.check(resp_err['action_type'], resp_err)
                            if resp_err['action_type'] == "wait_for_user_reply":
                                self._env.wait_for_user_reply = True
                                return messages.get_dict()
                        
                        if is_continue: continue
                elif cur_operation['action_type'] == "estimate_carbon_emission":
                    self._env.set_action(cur_operation['action_type'])
                    pg_name = self._env.get_variable("program_name")
                    if not pg_name:
                        # ask for program name
                        # ...
                        pg_name = "O0002" # 暫時寫死，之後改為從使用者訊息中取得
                    pg = Lib.Program(pg_name)
                    # emission_val = Lib.CarbonEmissionEstimator.Estimate(pg)
                    val_str = Lib.MemoryReader.Read(self.conn, "<mock memory address>")
                    val_f = eval("{0} {1}".format(val_str, "/ 1000"))
                    text = cur_operation['text'].format(pg.Name, val_f)
                    messages.add_message(text)
                elif cur_operation['action_type'] == "until_completed":
                    self._env.set_action(cur_operation['action_type'])
                    if cur_operation['task_type'] == "warmup":
                        self._env.set_action(cur_operation['task_type'])
                        StructureCheckerFactory.check(cur_operation['task_type'], cur_operation)
                        self._warmup_machine(cur_operation['params'])
                elif cur_operation['action_type'] == "check_tools_info_entered":
                    self._env.set_action(cur_operation['action_type'])
                    pg_name = self._env.get_variable("program_name")
                    pg_root = self._env.get_variable("program_root")
                    pg = Lib.Program(pg_name)
                    pg.Find(self.conn, pg_root)
                    tools = ProgramToolChecker.check(self.conn, pg)
                    self._env.set_variable("missing_tools", tools)
                elif cur_operation['action_type'] == "loop_events":
                    self._env.set_action(cur_operation['action_type'])
                    if "condition" in cur_operation:
                        condition = cur_operation['condition']
                        finish = cur_operation['finish']
                        self._env.set_action(condition['action_type'])
                        StructureCheckerFactory.check("base", condition)
                        StructureCheckerFactory.check(condition['action_type'], condition)
                        if condition['action_type'] == "check_var":
                            value = self._env.get_variable(condition['field'])
                            std = condition['standard']
                            if not eval(f'{value} {std}'):
                                self._env.set_action(finish['action_type'])
                                StructureCheckerFactory.check("base", finish)
                                StructureCheckerFactory.check(finish['action_type'], finish)
                                if finish['action_type'] == "jump_to":
                                    self._env.step = finish['step']
                                    continue

                        for event in cur_operation['events']:
                            self._env.set_action(event['action_type'])
                            StructureCheckerFactory.check("base", event)
                            StructureCheckerFactory.check(event['action_type'], event)
                            if event['action_type'] == "copy_var":
                                var = self._env.get_variable(event['source'])
                                item = var[event['index']] if var else ""
                                self._env.set_variable(event['dest'], item)
                            elif event['action_type'] == "echo":
                                text = event['text']
                                if "format" in event and event['format']:
                                    items = [self._env.get_variable(k) for k in event['format']]
                                    text = event['text'].format(*items)
                                messages.add_message(text)
                            elif event['action_type'] == "wait_for_user_reply":
                                self._env.wait_for_user_reply = True
                elif cur_operation['action_type'] == "check_program_execution_record":
                    self._env.set_action(cur_operation['action_type'])
                    pg_name = self._env.get_variable("program_name")
                    text = "There is no record of activating the program {0}. \nFirst article inspection is recommended.".format(pg_name)
                    messages.add_message(text)
                else:
                    raise NoActionTypeError(cur_operation['action_type'])
                '''next step of workflow'''
                is_end = self._env.next_step()
            else:
                '''使用者嘗試開啟指定作業流程'''
                if "machine condition" in user_message:
                    self._setup_script("machine_inspection")
                elif "warm" in user_message:
                    self._setup_script("warm_up")
                elif "machine process" in user_message:
                    self._setup_script("machine_processing")
                else:
                    prompt = PromptTemplateFactory.format("QA", user_message)
                    (is_ok, result) = self._gpt.completion(prompt)
                    if not is_ok:
                        self._env.wait_for_user_reply = True
                        text = (result + " Please say it again.").strip()
                        messages.add_message(text, MessageColor.AI_WARNING)
                    else:
                        messages.add_message(result)
                    return messages.get_dict()
        return messages.get_dict()
    
    def _load_script(self, name: str) -> Dict[str, Any]:
        file_path = os.path.join(os.getcwd(), os.getenv("SCRIPT_PATH"), f'{name}.json')
        if not os.path.isfile(file_path): return {}
        return load_json(file_path)

    def _setup_script(self, name: str):
        script = self._load_script(name)
        self._env.state = name
        self._env.set_script(script)
        if "workflow" in script:
            self._env.set_workflow(script['workflow'])
            if self._env.exist_breakpoint():
                self._env.setup_breakpoint()
            else:
                self._env.step = script["workflow"][0]

    def _exit_script(self, save: bool):
        if save:
            self._env.save_breakpoint()
        else:
            self._env.remove_breakpoint()
        self._env.state = ""
        self._env.step = ""
        self._env.clear_script()
        self._env.clear_workflow()
        self._env.clear_variable()
        self._env.claer_action_history()
        self._env.wait_for_user_reply = False
    
    def _warmup_machine(self, obj: Dict[str, Any]) -> None:
        self.worker = WarmUpWorker(self.conn, obj['path'], obj['standard'], self._callback)
        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)
        self.worker.finished.connect(self.workerThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.workerThread.started.connect(self.worker.do_task)
        self.workerThread.start()