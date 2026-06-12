from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from model import predict

from database.db import SessionLocal
from database.models import Prediction
from database.deps import get_db

from auth import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print("TOKEN:", credentials.credentials)
    print("HEADERS:", credentials)
    print("TYPE:", type(credentials))

    token = credentials.credentials
    payload = decode_token(token)
    return payload["user_id"]



@router.post("/predict")
async def predict_image(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    image_bytes = await file.read()

    result = predict(image_bytes)

    if not result["success"]:
        return result

    face = result["faces"][0]

    prediction = Prediction(
        user_id=user_id,
        age=face["age"],
        gender=face["gender"],
        age_confidence=face["age_confidence"],
        gender_confidence=face["gender_confidence"]
    )

    db.add(prediction)
    db.commit()

    return result