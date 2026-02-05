from fastapi import APIRouter
from psycopg import connect
from app.core.config import settings

router = APIRouter()

@router.get("/health/db")
def health_db():
    try:
        with connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            connect_timeout=3,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "degraded", "db": "down", "error": str(e)}
