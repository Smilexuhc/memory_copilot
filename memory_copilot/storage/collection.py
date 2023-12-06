import os
import json
from datetime import datetime
from typing import List

from peewee import *

from memory_copilot.storage.model import Collection

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class CollectionDBModel(BaseModel):
    """
    Collection is the basic unit of memory.
    """
    id = AutoField()
    user_input = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    title = TextField()
    abstract = TextField()
    keywords = TextField()
    metadata = TextField(null=True)

    @staticmethod
    def create_collection(user_input: str,
                          collection: Collection):
        return CollectionDBModel.create(
            user_input=user_input,
            title=collection.title,
            abstract=collection.abstract,
            keywords=','.join(collection.keywords),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata=json.dumps(collection.metadata)
        )

    @staticmethod
    def list_collections() -> List['CollectionDBModel']:
        return CollectionDBModel.select().order_by(CollectionDBModel.id.desc())

    @staticmethod
    def get_collections(ids: List[int]) -> List['CollectionDBModel']:
        data = CollectionDBModel.select().where(CollectionDBModel.id.in_(ids))
        return data.execute()

    @staticmethod
    def delete_collection(id: int):
        CollectionDBModel.delete().where(CollectionDBModel.id == id).execute()

    @staticmethod
    def to_json(data: 'CollectionDBModel'):
        return {
            'id': data.id,
            'user_input': data.user_input,
            'created_at': data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': data.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'title': data.title,
            'abstract': data.abstract,
            'keywords': data.keywords.split(','),
            'metadata': json.loads(data.metadata) if data.metadata else {}
        }


def setup_db(db_dir: str):
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    db.init(f'{db_dir}/collections.db', pragmas={'journal_mode': 'wal'})
    db.connect()
    db.create_tables([CollectionDBModel])
