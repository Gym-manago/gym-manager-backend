from typing import Annotated
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health_check, auth, member
from app.dependencies import oauth2_scheme

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gym-manager-chirawa-dev.vercel.app",
                   "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "POST"],
    allow_headers=["*"],
)

app.include_router(health_check.router)
app.include_router(auth.router)
app.include_router(member.router)


@app.get("/token/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
