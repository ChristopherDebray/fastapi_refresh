from fastapi import APIRouter

router = APIRouter(prefix="", tags=["system"])

@router.get("/health_check")
async def root():
    return {
        "status": "healthy",
    }
