from pydantic import BaseModel, Field
from uuid import UUID


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserModelBase(BaseModel):
    username: str = Field()
    email: str

class LoginResponse(UserModelBase,TokenResponse):
    pass
class UserModelWithPassword(UserModelBase):
    password: str


class UserModelResponse(UserModelBase):
    id: UUID
