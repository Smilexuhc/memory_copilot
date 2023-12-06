import json


def parse_llm_response(response: str) -> dict:
    return json.loads(response)
