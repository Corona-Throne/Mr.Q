import os
from dotenv import load_dotenv
from typing import Tuple
load_dotenv()

from openai import AzureOpenAI, BadRequestError

from src.model.utile.singleton import SingletonMeta
from src.model.error.printer import ErrorPrinter


class IChatModel(metaclass=SingletonMeta):
    def __init__(self) -> "IChatModel":
        self._engine: AzureOpenAI = None
        self._model: str = None, # model = "deployment_name".
        self._temperature = 0.7
        self._timeout = 40 # 暫時沒用

    def completion(self, text: str) -> Tuple[bool, str]:
        if self._engine is None: raise ValueError("engine is not defined.")
        try:
            response = self._engine.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "user", "content": text}
                ],
                temperature=self._temperature,
            )
            return (True, response.choices[0].message.content)
        except BadRequestError as brex:
            ErrorPrinter.print("User message triggers Azure OpenAI's content management policy.", className=self.__class__.__name__)
            return (False, "Your message triggers Azure OpenAI's content management policy.")
        except Exception as ex:
            ErrorPrinter.print(ex, className=self.__class__.__name__)
            return (False, "")
    
class GPT35(IChatModel):
    def __init__(self, temperature: float=0.3, timeout: int=20) -> "GPT35":
        super().__init__()
        self._engine = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),
            api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_API_BASE")
        )
        self._model = os.getenv("AZURE_LIGHT_DEPLOYMENT_NAME")
        self._temperature = temperature
        self._timeout = timeout