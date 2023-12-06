import json

from memory_copilot.llm import ChatMessages, ChatOpenAI


def detect_action(text: str) -> str:
    llm = ChatOpenAI()
    prompt = """
As a Memory Co-Pilot Agent, your role is to assist the user in managing their memory. This will entail analyzing the user's action type. Below are the action types and their respective descriptions:

1. query: This action is initiated when the user desires to retrieve information from their memory.
2. memorize: User wishes to commit something to memory. Examples include: "Mark an article", "Collect the webpage" and etc.
3. unknown: User's action cannot be clearly identified.

You should only respond in JSON format as described below
Response Format:
{
    'action': 'query'
    'reason': 'Your reasoning for the action'
}
Ensure the response can be parsed by Python json.loads
"""
    messages = ChatMessages(
        system_message=prompt
    )
    messages.add_user_message(text)
    res = llm.chat(messages, model='gpt-4-1106-preview', max_tokens=1000)
    res_json = json.loads(res)
    return res_json['action'], res_json['reason']
