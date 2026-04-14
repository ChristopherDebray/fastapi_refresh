from fastapi import APIRouter

from app.core.routing import PublicAPIRoute

router = APIRouter(prefix="", tags=["system"], route_class=PublicAPIRoute)

@router.get("/health_check")
async def root():
    return {
        "status": "healthy",
    }
