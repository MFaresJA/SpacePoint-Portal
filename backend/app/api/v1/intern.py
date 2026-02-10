from fastapi import APIRouter, Depends
from app.deps.roles import require_roles

router = APIRouter()

@router.get("/ping")
def intern_ping(user=Depends(require_roles("intern", "admin"))):
    return {"ok": True, "msg": "intern access granted"}
