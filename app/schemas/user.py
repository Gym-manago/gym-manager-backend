from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class UserSchema(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True)
    email: str
    password: str
