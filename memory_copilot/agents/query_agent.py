import json
from dataclasses import dataclass
from string import Template
from typing import Optional

from memory_copilot.llm import ChatMessages, ChatOpenAI
from memory_copilot.tools import TOOLS, exec_tool, generate_prompts

SETTING_PROMPT = """
As a Collection Query Copilot, your primary responsibility is to handle user requests for retrieving potential collections from the collection storage.
The query results should be presented as a list of collection IDs, data format is described below.
```
@dataclass
class QueryResult:
    ids: list[int]
```


To perform this task, you are provided with various tools for retrieving collections from the database.
Upon successful retrieval of the corresponding collections, please submit your findings using the 'submit_result' tool.
Ensure that the final result is presented in JSON format.

Tools:
$tool_prompt

Principles:
1. Think step by step and reason yourself to the right decisions to make sure we get it right.
2. You can use the tools to help you, exclusively use the tools listed in double quotes e.g. "command name".
3. Your output should be succinct, cause every token is expensive.

Performance Evaluation:
1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.
2. Constructively self-criticize your big-picture behavior constantly.
3. Reflect on past decisions and strategies to refine your approach.

You should only respond in JSON format as described below
Response Format:
{
    "thoughts": {
        "text": "thought",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
    },
    "command": {
        "name": "command name",
        "args": {
            "argument name": "value"
        }
    }
}
Ensure the response can be parsed by Python json.loads
"""


@dataclass
class QueryResult:
    ids: list[int]


class QueryAgent:
    MODEL = 'gpt-4-1106-preview'
    ACCESS_TOOLS = [
        'list_memory',
        'submit_result',
        'get_current_datatime'
    ]

    def __init__(self):
        self._llm = ChatOpenAI()
        self._tools = {
            name: TOOLS[name] for name in self.ACCESS_TOOLS
        }
        prompt = Template(SETTING_PROMPT).substitute(
            tool_prompt=generate_prompts(list(self._tools.values())))
        self._messages = ChatMessages(prompt)
        print('Initializing agent...')
        self._result = None

    @property
    def finished(self):
        return self._result is not None

    def get_result(self):
        return self._result[0]

    def run_step(self, user_prompt: Optional[str] = None):
        if user_prompt is not None:
            self._messages.add_user_message(user_prompt)

        reply = self._llm.chat(
            self._messages, model='gpt-4-1106-preview', max_tokens=500)
        reply_json = json.loads(reply)
        self._messages.add_assistant_message(reply)
        print(f'AI: {reply}')
        try:
            command = reply_json['command']['name']
            args = reply_json['command']['args']
            if command == 'submit_result':
                args['result_type'] = QueryResult
            result, result_str, status = exec_tool(self._tools, command, **args)
        except Exception as e:
            print(f'Error occurred when executing tool, error:\n{str(e)}')
            result_str = f'Error occurred when executing tool, error:\n{str(e)}'
            raise e
        print(f'Exec tool: {result_str}')
        if command == 'submit_result':
            self._result = result
        self._messages.add_user_message(result_str)
