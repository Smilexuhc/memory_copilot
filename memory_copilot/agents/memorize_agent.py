import json
from string import Template
from typing import Optional

from memory_copilot.llm import ChatMessages, ChatOpenAI
from memory_copilot.storage.model import Collection
from memory_copilot.tools import TOOLS, exec_tool, generate_prompts

SETTING_PROMPT = """
Your are a service capable of extracting information from a user request to store a collection in the database.
The user request will include details about the memory that need to be extracted and processed.

The schema of the collection to be stored is as follows:
- title: The title of the collection
- abstract: The abstract or summary of the collection
- keywords: The keywords associated with the collection
- metadata: Any other information that is relevant to the collection, e.g. author, source, address, etc. Stored as a JSON string.

If the user request is incomplete, you are permitted to use supplementary tools to fill in the missing information. 
Once you have extracted and processed the necessary details, submit your results using the 'submit_result' tool. 
Ensure that the final result is presented in JSON format.

Tools:
$tool_prompt

Principles:
1. Think step by step and reason yourself to the right decisions to make sure we get it right.
2. You can use the tools to help you, exclusively use the tools listed in double quotes e.g. "command name".
3. Your output should be succinct, cause every token is expensive.
4. Do not ask for help from human as possible as you can.

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


class MemorizeAgent:
    # TODO(Smile): Abstract base agent class
    MODEL = 'gpt-4-1106-preview'
    ACCESS_TOOLS = [
        'crawl_web',
        'read_file',
        'read_pdf',
        'submit_result',
        'ask_human',
        'exit_task',
    ]

    def __init__(self, retry_iters: int = 3):
        self._llm = ChatOpenAI()
        self._tools = {
            name: TOOLS[name] for name in self.ACCESS_TOOLS
        }
        prompt = Template(SETTING_PROMPT).substitute(
            tool_prompt=generate_prompts(list(self._tools.values())))
        self._messages = ChatMessages(prompt)
        print('Initializing agent...')
        self._result = None
        self._error_iter = 0
        self._retry_iters = retry_iters
        self._status = 'running'

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
        reply = self._llm.chat(self._messages, model=MemorizeAgent.MODEL, max_tokens=1000)
        reply_json = json.loads(reply)
        self._messages.add_assistant_message(reply)
        print(f'AI:\n{reply}')
        command = reply_json['command']['name']
        args = reply_json['command']['args']
        if command == 'submit_result':
            args['result_type'] = Collection
        result, result_str, tool_status = exec_tool(self._tools, command, **args)
        print(f'Tool Result:\n{result_str}')
        if tool_status:
            self._reset_error_iter()
            if command == 'exit_task':
                print(f'Failed to complete task, reason: {result}')
                self._status = 'failed'
            if command == 'submit_result':
                self._result = result  # result and reason
                self._status = 'success'
        else:
            self._error_iter += 1
        if self._error_iter >= self._retry_iters:
            self._status = 'failed'
            print(f'Retry limit reached')
        self._messages.add_user_message(result_str)
