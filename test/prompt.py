prompt = """According to the user's message, extract the name of program, i.e. O0002

<User response>
i would like to download O0003
</User response>

Answer: """

import os
import sys
sys.path.append(os.getcwd())
from src.model.chat.azure import GPT35
gpt = GPT35(temperature=0.7)
(is_ok, result) = gpt.completion(prompt)
print(is_ok)
print(result)