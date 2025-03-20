from typing import Annotated

from fastapi import FastAPI, Depends, Query, status
from fastapi.exceptions import HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

from contextlib import asynccontextmanager


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass


app = FastAPI(lifespan=lifespan)


"""deprecated"""
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes/", response_model=list[Hero])
def read_heroes(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} not found!",
        )
    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {hero_id} not found!",
        )
    session.delete(hero)
    session.commit()
    return {"ok": True}
