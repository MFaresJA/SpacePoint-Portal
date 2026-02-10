from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.auth import get_current_user



from app.deps.db import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserMeResponse,
)
from app.services.auth_service import (
    get_user_by_email,
    create_user,
    authenticate_user,
    generate_access_token,
)
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = create_user(db, payload.email, payload.password)
    token = generate_access_token(user)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = generate_access_token(user)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserMeResponse)
def me(current_user: User = Depends(get_current_user)):
    # Placeholder — we will inject current_user via JWT dependency in next step
    return UserMeResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        is_suspended=current_user.is_suspended,
    )
