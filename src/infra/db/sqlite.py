import os
from sqlmodel import SQLModel, create_engine, Session

from config import CONFIG


engine = create_engine(CONFIG.database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
