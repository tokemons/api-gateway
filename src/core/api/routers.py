from fastapi import APIRouter

from src.modules.auth.routers import router as auth_router

__all__ = ("router",)

router = APIRouter()
router.include_router(auth_router)


@router.get("/health")
async def health_route() -> None: ...
