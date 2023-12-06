from memory_copilot.agents import MemorizeAgent, QueryAgent
from memory_copilot.storage import CollectionDBModel
from memory_copilot.tools import detect_action
from memory_copilot.utils import show_table


def memorize_pipeline(user_request: str):
    agent = MemorizeAgent()
    agent.run_step(user_request)
    while agent.status == 'running':
        agent.run_step()
    if agent.status == 'failed':
        print('Failed to complete task')
        return
    result = agent.get_result()
    print(f'Final result:\n{result}')
    CollectionDBModel.create_collection(
        user_input=user_request,
        collection=result
    )
    print('Collection saved')


def query_pipeline(user_request: str):
    agent = QueryAgent()
    agent.run_step(user_request)
    while not agent.finished:
        agent.run_step()
    result = agent.get_result()
    collections = CollectionDBModel.get_collections(result.ids)
    show_table(collections)


def pipeline(user_request: str):
    print('Task starting...')
    print('Detecting intention...')
    intention, reason = detect_action(user_request)
    if intention == 'query':
        query_pipeline(user_request)
    elif intention == 'memorize':
        memorize_pipeline(user_request)
    else:
        print(f'Unknown intention with reason {reason}')
        exit(1)
