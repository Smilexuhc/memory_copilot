from typing import Any


class AgentMemory:

    def __init__(self):
        self._memory = {}

    def store(self, name: str, value: Any):
        if name in self._memory:
            raise ValueError(f'Memory name {name} already exists')
        self._memory[name] = value

    def get(self, name: str) -> Any:
        if name not in self._memory:
            raise ValueError(f'Memory name {name} not exists')
        return self._memory[name]
