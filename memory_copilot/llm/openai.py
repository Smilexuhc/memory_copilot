import os
from typing import Optional

import openai
from retry import retry

from memory_copilot.llm import ChatMessages


def setup_openai(api_key: Optional[str] = None, api_base: Optional[str] = None):
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = api_key
    if api_base is not None:
        openai.api_base = api_base


class ChatOpenAI:

    def __init__(self):
        pass

    @retry(tries=3, delay=0.1)
    def chat(self,
             chat_messages: ChatMessages,
             model: str,
             max_tokens: int = 1000,
             temperature: float = 0.7,
             frequency_penalty: int = 0,
             presence_penalty: int = 0,
             json_mode: bool = True):
        reply = openai.ChatCompletion.create(
            model=model,
            messages=chat_messages.messages,
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            response_format={'type': 'json_object'} if json_mode else None,
        )
        return reply['choices'][0]['message']['content']
