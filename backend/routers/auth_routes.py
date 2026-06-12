from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import User
from database.deps import get_db

from schemas.user import RegisterRequest, LoginRequest

from auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == request.email).first()

    if existing:
        return {"success": False, "message": "Email already exists"}

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(request.password)
    )

    db.add(user)
    db.commit()

    return {"success": True}


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        return {"success": False, "message": "Invalid credentials"}

    if not verify_password(request.password, user.password):
        return {"success": False, "message": "Invalid credentials"}

    token = create_access_token({"user_id": user.id})

    return {
        "success": True,
        "token": token,
        "username": user.username
    }

