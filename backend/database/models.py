from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database.db import Base

from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True, index=True)
    
    email = Column(String, unique=True, index=True)

    password = Column(String(255), nullable=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    age = Column(String)

    gender = Column(String)

    age_confidence = Column(Float)

    gender_confidence = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )