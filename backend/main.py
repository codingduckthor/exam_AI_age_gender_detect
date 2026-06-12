from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine
from database.models import Base

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers.auth_routes import router as auth_router
from routers.predict_routes import router as predict_router
from routers.history_routes import router as history_router

# создать таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# подключаем роутеры
app.include_router(auth_router)
app.include_router(predict_router)
app.include_router(history_router)