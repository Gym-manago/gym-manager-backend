from sqlmodel import SQLModel, create_engine
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASS}@{POSTGRES_HOST}/{DB_NAME}"
)

print(">>>>>>", DATABASE_URL)
engine = create_engine(DATABASE_URL)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield
    pass
