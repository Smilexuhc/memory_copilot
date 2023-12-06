from memory_copilot.storage import CollectionDBModel
from memory_copilot.tools import register_meta


@register_meta('List all stored memory', returns={'memory': 'List[dict]'})
def list_memory():
    collections = CollectionDBModel.list_collections()
    return [CollectionDBModel.to_json(collection) for collection in collections]
