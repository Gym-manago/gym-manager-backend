from typing import Annotated
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health_check, auth
from app.database import lifespan
from app.dependencies import oauth2_scheme

load_dotenv()


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
