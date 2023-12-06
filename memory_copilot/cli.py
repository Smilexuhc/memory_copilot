import os
import json
from typing import Optional

import click

from memory_copilot.llm import setup_openai
from memory_copilot.pipeline import pipeline
from memory_copilot.storage import setup_db, CollectionDBModel
from memory_copilot.utils import show_table

DB_PATH = os.path.join(os.path.dirname(__file__), 'db')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('request')
@click.option('--api_key', type=str, default=None)
def chat(request: str, api_key: Optional[str]):
    setup_openai(api_key)
    setup_db(DB_PATH)
    pipeline(request)


@cli.command()
def show():
    setup_db(DB_PATH)
    collections = CollectionDBModel.list_collections()
    show_table(collections)


@cli.command()
@click.argument('dump_path')
def dump(dump_path: str):
    setup_db(DB_PATH)
    collections = CollectionDBModel.list_collections()
    collection_dict_list = [
        CollectionDBModel.to_json(item) for item in collections]
    with open(dump_path, 'w') as f:
        json.dump(collection_dict_list, f)


@cli.command()
@click.argument('id')
def delete(id: str):
    setup_db(DB_PATH)
    CollectionDBModel.delete_collection(id)
    print(f'Deleted collection {id} successfully.')


@cli.command()
def clear():
    setup_db(DB_PATH)
    CollectionDBModel.clear_collections()
    print(f'All collections are deleted successfully.')


if __name__ == '__main__':
    cli()
