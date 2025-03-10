from src.model.prompt.template import *

class PromptTemplateFactory:

    @staticmethod
    def format(tybe: str, *args) -> str:
        if tybe == "user_message":
            return UserMessagePromptTemplate.format(*args)
        elif tybe == "QA":
            return QAPromptTemplate.format(*args)