from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class UserModelBase(SQLModel):
    username: str = Field(index=True)
    email: str


class UserSchema(UserModelBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password: str


class UserModelResponse(UserModelBase):
    id: UUID


class TokenResponse(SQLModel):
    access_token: str
    token_type: str


class LoginResponse(UserModelBase, TokenResponse):
    pass
