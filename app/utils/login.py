from passlib.context import CryptContext
from app.dependencies import SessionDep
from sqlmodel import select
from app.schemas.user import UserSchema
from datetime import timedelta, datetime
import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, session: SessionDep) -> bool:
    user = session.exec(select(UserSchema).where(UserSchema.username == username)).one()
    if not user or not verify_password(password, user.password):
        return False
    return True


def create_access_token(data: dict, expires_delta: timedelta):
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    data.update({"exp": expire})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token
