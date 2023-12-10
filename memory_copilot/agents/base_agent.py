import json
from dataclasses import dataclass
from string import Template
from typing import Optional

from memory_copilot.tools import TOOLS, exec_tool, generate_prompts
from memory_copilot.llm import ChatMessages, ChatOpenAI


class BaseTaskAgent:
    # TODO(Smile): use prompt template

    AGENT_PROMPT = ''
    ACCESS_TOOLS = []
    RESULT_TYPE: dataclass = None

    def __init__(self,
                 model: str = 'gpt-4-1106-preview',
                 max_token: int = 1000,
                 retry_iters: int = 3):
        agent_name = self.__class__.__name__
        print(f'Initializing agent {agent_name} ...')
        self._llm = ChatOpenAI()
        self._model = model
        self._max_token = max_token
        self._tools = {name: TOOLS[name] for name in self.ACCESS_TOOLS}
        # init system prompt
        init_prompt = Template(self.AGENT_PROMPT).substitute(
            tool_prompt=generate_prompts(list(self._tools.values()))
        )
        self._messages = ChatMessages(init_prompt)

        # init agent status
        self._result, self._status = None, 'running'
        self._error_iter, self._retry_iters = 0, retry_iters

    def _reset_error_iter(self):
        self._error_iter = 0

    @property
    def status(self):
        return self._status

    def get_result(self):
        return self._result[0]

    def run_step(self, user_prompt: Optional[str] = None):
        if user_prompt is not None:
            self._messages.add_user_message(user_prompt)
        reply = self._llm.chat(self._messages, model=self.MODEL, max_tokens=self._max_token)
        reply_json = json.loads(reply)
        self._messages.add_assistant_message(reply)
        print(f'AI:\n{reply}')
        command = reply_json['command']['name']
        args = reply_json['command']['args']
        if command == 'submit_result':
            args['result_type'] = self.RESULT_TYPE
        result, result_str, tool_status = exec_tool(self._tools, command, **args)
        print(f'Tool Result:\n{result_str}')
        if tool_status:
            self._reset_error_iter()
            if command == 'exit_task':
                print(f'Failed to complete task, reason: {result}')
                self._status = 'failed'
                self._reason = result
            if command == 'submit_result':
                self._result = result  # result and reason
                self._status = 'success'
        else:
            self._error_iter += 1
        if self._error_iter >= self._retry_iters:
            self._status = 'failed'
            print(f'Retry limit reached')
        self._messages.add_user_message(result_str)
