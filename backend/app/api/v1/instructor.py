from fastapi import APIRouter, Depends
from app.deps.roles import require_roles

router = APIRouter()

@router.get("/ping")
def instructor_ping(user=Depends(require_roles("instructor", "admin"))):
    return {"ok": True, "msg": "instructor access granted"}
