import json
from typing import List

from rich.console import Console
from rich.table import Table

from memory_copilot.storage import CollectionDBModel


def show_table(collections: List[CollectionDBModel]):
    table = Table(title='Collections')
    table.add_column('ID')
    table.add_column('Title')
    table.add_column('Abstract')
    table.add_column('Keywords')
    table.add_column('Create Time')
    table.add_column('Metadata')
    for collection in collections:
        data_json = CollectionDBModel.to_json(collection)
        metadata = data_json['metadata'] if isinstance(
            data_json['metadata'], str) else json.dumps(data_json['metadata'])
        table.add_row(
            str(data_json['id']),
            data_json['title'],
            data_json['abstract'],
            ', '.join(data_json['keywords']),
            data_json['created_at'],
            metadata
        )
    console = Console()
    console.print(table)
