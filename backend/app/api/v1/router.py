from fastapi import APIRouter

from app.api.v1 import auth, instructor, ambassador, intern, admin, content, leaderboard, health


api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(instructor.router, prefix="/instructor", tags=["instructor"])
api_v1_router.include_router(ambassador.router, prefix="/ambassador", tags=["ambassador"])
api_v1_router.include_router(intern.router, prefix="/intern", tags=["intern"])
api_v1_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(content.router, prefix="/content", tags=["content"])
api_v1_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
api_v1_router.include_router(health.router, tags=["health"])
