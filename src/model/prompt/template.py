from src.model.prompt.base import PromptTemplate

class UserMessagePromptTemplate(PromptTemplate):
    
    @staticmethod
    def format(prompt: str, user_msg: str) -> str:
        return (
            "{0}\n"
            "\n<User Message>\n"
            "{1}"
            "\n</User Message>\n"
            "\nAnswer: "
        ).format(prompt, user_msg)

class QAPromptTemplate(PromptTemplate):

    @staticmethod
    def format(user_msg: str) -> str:
        return (
            "You are a CNC machine assistant, responsible for answering users' machine-related questions.\n"
            "Answer the question and keep the answer short and concise. \n"
            # "Respond \"Sorry, I don't know the answer. Please ask our service staff.\" if not sure about the answer.\n"
            "Question: {0}\n"
            "Answer: "
        ).format(user_msg)