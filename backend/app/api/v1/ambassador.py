from fastapi import APIRouter, Depends
from app.deps.roles import require_roles

router = APIRouter()

@router.get("/ping")
def ambassador_ping(user=Depends(require_roles("ambassador", "admin"))):
    return {"ok": True, "msg": "ambassador access granted"}
