import uuid
from typing import List

import databases
import sqlalchemy
from sqlalchemy import create_engine

from . import constants

database = databases.Database(constants.SQLALCHEMY_DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(length=100)),
    sqlalchemy.Column("contents", sqlalchemy.String(length=100)),
)
engine = create_engine(
    constants.SQLALCHEMY_DATABASE_URL
)
metadata.create_all(engine)


# CRUD Methods
async def get_notes(ids: List[int]):
    query = notes.select().where(notes.c.id.in_(ids))
    return await database.fetch_all(query)


async def create_note(id: int, title="title", contents="contents"):
    query = notes.insert().values(id=id, title=title, contents=contents)
    return await database.execute(query)


async def delete_notes(ids: List[int]):
    query = notes.delete().where(notes.c.id.in_(ids))
    return await database.execute(query)


async def make_fetch_then_delete_objects():
    # create
    ids = [uuid.uuid4().int & (1 << 31) - 1 for i in range(constants.NUMBER_OF_ITEMS_FOR_DATABASE)]
    for id in ids:
        await create_note(id)

    # fetch
    await get_notes(ids)

    # delete
    await delete_notes(ids)
