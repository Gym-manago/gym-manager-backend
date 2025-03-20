from fastapi import APIRouter

router = APIRouter()


@router.get("/health_check")
def root():
    return {"status": "ok"}
