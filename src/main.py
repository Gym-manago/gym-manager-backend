from fastapi import FastAPI, Body, Cookie, Header
from pydantic import BaseModel, Field

from typing import Annotated

app = FastAPI()


class ItemModel(BaseModel):
    a: int = Field(title="This is a numeric value", examples=[1])
    b: int = Field(title="This is another numeric value")


class MoreItem(BaseModel):
    c: int = Field(title="This is a numeric value")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items/{item_id}")
def post_items(
    item_id: str, items: ItemModel, new_items: MoreItem, q: str | None = None
):
    return {"value": items.a + items.b + new_items.c, "item_id": item_id, "q": q}


@app.post("/name")
def post_name(
    name: Annotated[str, Body()],
    age: Annotated[int, Body()],
    csrf_token: Annotated[str, Cookie()],
    user_agent: Annotated[str, Header(convert_underscores=True)],
):
    return {
        "name": name,
        "age": age,
        "csrf_token": csrf_token,
        "user_agent": user_agent,
    }
