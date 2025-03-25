from fastapi.security import OAuth2PasswordBearer
from .database import engine
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
