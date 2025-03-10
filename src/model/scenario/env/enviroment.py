from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class Enviroment:
    state: str = field(default="")
    step: str = field(default="")
    _workflow: List[str] = field(default_factory=list)
    _script: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    _breakpoint: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    _global_var: Dict[str, Any] = field(default_factory=dict)
    _variable: Dict[str, Any] = field(default_factory=dict)
    _action_history: List[str] = field(default_factory=list)
    wait_for_user_reply: bool = field(default=False)

    ########################################
    #               workflow               #
    ########################################
    def set_workflow(self, workflow: List[str]) -> None:
        self._workflow = workflow

    def clear_workflow(self) -> None:
        self._workflow = list()

    ########################################
    #                script                #
    ########################################
    def set_script(self, script: Dict) -> None:
        self._script = script
    
    def get_cur_operation(self) -> Dict:
        if self.step not in self._script: return {}
        return self._script[self.step]

    def clear_script(self) -> None:
        self._script = dict()

    ########################################
    #              breakpoint              #
    ########################################
    def save_breakpoint(self) -> None:
        if self.state in self._breakpoint:
            self.remove_breakpoint()
        self._breakpoint[self.state] = {}
        self._breakpoint[self.state]['step'] = self._last_step()
        if self._variable:
            self._breakpoint[self.state]['var'] = self._variable

    def exist_breakpoint(self) -> bool:
        if self.state not in self._breakpoint: return False
        return True
    
    def setup_breakpoint(self) -> None:
        if self.state not in self._breakpoint: return
        if "step" in self._breakpoint[self.state]:
            self.step = self._breakpoint[self.state]['step']
        if "var" in self._breakpoint[self.state]:
            self._variable = self._breakpoint[self.state]['var']

    def remove_breakpoint(self) -> None:
        if self.state in self._breakpoint:
            del self._breakpoint[self.state]

    ########################################
    #            global variable           #
    ########################################
    def set_global_var(self, key: str, val: Any) -> None:
        self._global_var[key] = val
    
    def get_global_var(self, key: str) -> Any:
        if key not in self._global_var: return None
        return self._global_var[key]
    
    def remove_global_var(self, key: str) -> None:
        if key in self._global_var:
            del self._global_var[key]

    ########################################
    #           script's variable          #
    ########################################
    def set_variable(self, key: str, val: Any) -> None:
        self._variable[key] = val
    
    def get_variable(self, key: str) -> Any:
        if key not in self._variable: return None
        return self._variable[key]

    def clear_variable(self) -> None:
        self._variable = dict()

    ########################################
    #            action history            #
    ########################################
    def set_action_history(self, history: List[str]) -> None:
        self._action_history = history

    def set_action(self, action: str) -> None:
        # print(f'------[Action] {action}')
        self._action_history.append(action)
    
    def get_last_action(self) -> str:
        if len(self._action_history) == 0: return ""
        return self._action_history[-1]

    def claer_action_history(self) -> None:
        self._action_history = list()

    ########################################
    #                 step                 #
    ########################################
    def _last_step(self) -> str:
        index = self._workflow.index(self.step)
        step = self._workflow[index-1] if index > 0 else self._workflow[0]
        return step

    def next_step(self) -> bool:
        index = self._workflow.index(self.step)
        self.step = self._workflow[index+1] if index < len(self._workflow)-1 else ""
        # print(f'---[Step] {self.step}')
        if self.step:
            return False
        return True
        
