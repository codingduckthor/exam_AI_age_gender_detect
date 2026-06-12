from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Prediction
from database.deps import get_db

from jose import JWTError

from auth import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(credentials.credentials)
        return payload["user_id"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/history")
def get_history(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .all()
    )

    return [
        {
            "age": p.age,
            "gender": p.gender,
            "age_confidence": p.age_confidence,
            "gender_confidence": p.gender_confidence,
            "created_at": p.created_at
        }
        for p in predictions
    ]