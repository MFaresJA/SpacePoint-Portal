from fastapi import APIRouter

from app.api.v1 import auth, instructor, ambassador, intern, admin, content, leaderboard, health, application, admin_applications, admin_ambassador, admin_intern, points, admin_audit, admin_points, admin_overview, users, admin_content, opportunities, certificates, crm, badges

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(instructor.router, prefix="/instructor", tags=["instructor"])
api_v1_router.include_router(ambassador.router, prefix="/ambassador", tags=["ambassador"])
api_v1_router.include_router(intern.router, prefix="/intern", tags=["intern"])
api_v1_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(content.router, prefix="/content", tags=["content"])
api_v1_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(application.router, prefix="/application", tags=["application"])
api_v1_router.include_router(admin_applications.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(admin_ambassador.router, prefix="/admin/ambassador", tags=["admin"])
api_v1_router.include_router(admin_intern.router, prefix="/admin/intern", tags=["admin"])
api_v1_router.include_router(points.router, tags=["points"])
api_v1_router.include_router(admin_audit.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(admin_points.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(admin_overview.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
api_v1_router.include_router(admin_content.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
api_v1_router.include_router(certificates.router, prefix="/certificates", tags=["certificates"])
api_v1_router.include_router(crm.router, prefix="/crm", tags=["crm"])
api_v1_router.include_router(badges.router, prefix="/badges", tags=["badges"])