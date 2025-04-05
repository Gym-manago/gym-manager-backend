from sqlmodel import SQLModel, create_engine
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.settings.base import DATABASE_URL
from operator import attrgetter

load_dotenv()


engine = create_engine(DATABASE_URL)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield
    pass
