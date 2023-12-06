import json

from memory_copilot.llm import ChatMessages, ChatOpenAI
from memory_copilot.tools import register_meta

SETTING_PROMPT = """
As an expert reader, your task involves receiving an article, summarizing its main points, and extracting the article's pertinent keywords.
You also need to extract the most brilliant section of the article, each section can be several sentences long and you need to directly copy the raw words.

You should only respond in JSON format as described below
Response Format:
{
    'title': 'Title of the article'
    'summary': 'This is the summary of the article',
    'keywords': ['keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5']
    'highlights': [
        'This is the first highlight',
        'This is the second highlight',
    ]
}
Ensure the response can be parsed by Python json.loads
"""


@register_meta("""Summarize input article, extract summary, keywords and highlights, and return in JSON format,
                return format:
                {
                    'title': 'Title of the article'
                    'summary': 'Summary of the article',
                    'keywords': ['keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5']
                    'highlights': [
                        'This is the first highlight',
                        'This is the second highlight',
                        ]
                }""",
               returns={'result': 'dict'})
def summarize_article(article: str) -> dict:
    llm = ChatOpenAI()
    messages = ChatMessages(
        system_message=SETTING_PROMPT
    )
    messages.add_user_message(article)
    response = llm.chat(messages,
                        model='gpt-4-1106-preview',
                        max_tokens=1000)
    result_json = json.loads(response)
    return result_json
