import uuid
from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from . import constants

engine = create_engine(
    constants.SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    contents = Column(String)


def create_all_models() -> None:
    """
    Create all the models as necessary
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> SessionLocal:
    return SessionLocal()


# CRUD Methods
def get_notes_query(db: Session, ids: List[int]):
    return db.query(Note).filter(Note.id.in_(ids))


def get_notes(db: Session, ids: List[int]):
    return get_notes_query(db, ids).all()


def create_note(db: Session, id, title="title", contents="contents"):
    db_note = Note(id=id, title=title, contents=contents)
    db.add(db_note)
    db.commit()
    return db_note


def delete_notes(db: Session, ids: List[int]):
    get_notes_query(db, ids).delete(synchronize_session='fetch')
    db.commit()


def make_fetch_then_delete_objects():
    create_all_models()
    db = get_db()

    # create
    ids = [uuid.uuid4().int & (1 << 31) - 1 for i in range(constants.NUMBER_OF_ITEMS_FOR_DATABASE)]
    for id in ids:
        create_note(db, id)

    # fetch
    get_notes(db, ids)

    # delete
    delete_notes(db, ids)
    db.close()
