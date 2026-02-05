from fastapi import FastAPI
from app.api.v1.router import api_v1_router
import uuid
from fastapi import Request
from app.core.logging import setup_logging


app = FastAPI(title="SpacePoint Portal API")

setup_logging()

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_v1_router, prefix="/api/v1")
