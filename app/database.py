from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
from app.settings.base import DATABASE_URL

load_dotenv()


engine = create_engine(DATABASE_URL)


def create_db_tables():
    SQLModel.metadata.create_all(engine)
