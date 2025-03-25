from fastapi import APIRouter, Depends
from app.dependencies import oauth2_scheme

router = APIRouter(tags=["Health check"])


@router.get("/health_check", dependencies=[Depends(oauth2_scheme)])
def root():
    return {"status": "ok"}
