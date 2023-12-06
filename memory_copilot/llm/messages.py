from typing import List, Optional


class ChatMessages:

    def __init__(self, system_message: Optional[str] = None):
        self._messages = []
        if system_message is not None:
            self.add_system_message(system_message)

    def add_system_message(self, content: str):
        self._messages.append({'role': 'system', 'content': content})

    def add_user_message(self, content: str):
        self._messages.append({'role': 'user', 'content': content})

    def add_assistant_message(self, content: str):
        self._messages.append({'role': 'assistant', 'content': content})

    @property
    def messages(self) -> List[str]:
        return self._messages

    @property
    def text_format(self):
        return '\n\n'.join([f'{msg["role"]}: {msg["content"]}' for msg in self._messages])
