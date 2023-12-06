import json
from dataclasses import asdict, dataclass, is_dataclass
from inspect import signature
from typing import Dict, List, Optional, Tuple, Any

from memory_copilot.utils import UnhandledAgentException


@dataclass
class ToolMeta:
    name: str
    description: str
    args: Dict[str, str]
    returns: Dict[str, str]


def register_meta(description: str,
                  name: Optional[str] = None,
                  args: Optional[Dict[str, str]] = None,
                  returns: Optional[Dict[str, str]] = None):
    def wrapper(func):
        name_ = func.__name__ or name
        sig = signature(func)
        if args is None:
            args_ = {
                name: param.annotation.__name__ for name,
                param in sig.parameters.items()
            }
        else:
            args_ = args
        func.meta = ToolMeta(name_, description, args_, returns)
        return func
    return wrapper


def _gen_single_prompt(tool: ToolMeta):
    prompt = f'{tool.name}: "{tool.description}", args: '
    prompt += ', '.join([f'<{name}:{type}>' for name,
                        type in tool.args.items()])
    if tool.returns is None:
        prompt += f', returns: None'
    else:
        prompt += ', returns: '
        prompt += ', '.join([f'<{name}:{type}>' for name,
                            type in tool.returns.items()])
    return prompt


def generate_prompts(tools: List[callable]) -> str:
    prompt = ''
    for i, tool in enumerate(tools):
        prompt += f'{i+1}. {_gen_single_prompt(tool.meta)}\n'
    return prompt


def convert_result_to_string(name: str, returns: Optional[tuple]) -> str:
    if returns is None:
        return f'Execute tool `{name}` successfully, returns: None'
    content = f'Execute tool `{name}` successfully, returns:\n'
    if not isinstance(returns, tuple):
        returns = (returns,)
    for value in returns:

        if is_dataclass(value):
            value = asdict(value)
        content += f'{json.dumps(value)}\n'
    return content


def exec_tool(tools: dict, name: str, **kwargs) -> Tuple[Any, str]:
    if name not in tools:
        raise ValueError(f'Unknown tool: {name}')
    try:
        tool = tools[name]
        returns = tool(**kwargs)
        returns_str = convert_result_to_string(name, returns)
    except UnhandledAgentException as e:
        print('Meet agent unhandled exception:')
        raise e
    except Exception as e:
        return None, f'Error occurred when executing tool, error:\n{str(e)}', False
    return returns, returns_str, True
