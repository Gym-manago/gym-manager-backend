from typing import Annotated
from fastapi import FastAPI, Depends
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health_check, auth
from app.database import lifespan
from app.dependencies import oauth2_scheme

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health_check.router)
app.include_router(auth.router)


@app.get("/token/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
