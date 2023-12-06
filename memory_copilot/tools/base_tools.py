import datetime
import json
from dataclasses import dataclass, fields
from typing import Tuple

from prompt_toolkit import prompt as pt_prompt

from memory_copilot.tools import register_meta


@register_meta(description='Get current time',
               returns={'datetime': 'str'})
def get_current_datatime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@register_meta(description='Ask human question for help, ensuring that the question is either multiple-choice or gap-filling',
               returns={'answer': 'str'})
def ask_human(question: str) -> str:
    return pt_prompt(f'AI ask: {question}')


@register_meta(description='Exit the task for unexpected reason')
def exit_task(reason: str):
    return reason


@register_meta(description='Submit the final result',
               args={'result': 'json string format', 'reason': 'str'},
               returns={'result': 'str', 'reason': 'str'})
def submit_result(result: str, reason: str, result_type: dataclass) -> Tuple[dataclass, str]:
    # TODO(Smile): Add validation for result
    result_dict = json.loads(result)
    filed_names = [f.name for f in fields(result_type)]
    if not all([k in filed_names for k in result_dict.keys()]):
        raise ValueError(f'Keys of result {result_dict.keys()} '
                         f'not match with {filed_names}')
    result = result_type(**result_dict)
    return result, reason
