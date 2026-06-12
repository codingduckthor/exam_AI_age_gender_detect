# AI Age & Gender Detection Project
## 1. Описание проекта + функциональные возможности

Проект представляет собой веб-приложение, использующее нейросетевую модель для определения возраста и пола человека по загруженному изображению.

Основной функционал:
Загрузка изображения через веб-интерфейс
Отправка изображения на backend API
Обработка изображения с помощью ML модели
Возврат результата:
Предсказанный возраст
Предсказанный пол
Авторизация пользователя (JWT / session-based — если реализовано)
История запросов пользователя (если подключена БД)
UI отображение результата в реальном времени

## 2. Архитектура проекта

Проект построен по клиент-серверной архитектуре:

```
Frontend (React + Vite)
        ↓ HTTP (REST API)
Backend (FastAPI / Flask)
        ↓
ML Model (PyTorch / OpenCV pipeline)
        ↓
(опционально) Database (PostgreSQL + SQLAlchemy)
```

Поток данных:
        1) Пользователь загружает изображение
        2) Frontend отправляет POST /predict
        3) Backend:
              декодирует изображение
              прогоняет через модель
              формирует результат
        4) Ответ возвращается на frontend

## 3. Использованные технологии
        Frontend:
        React (Vite)
        Axios (HTTP запросы)
        React Router DOM
        CSS / Flexbox / custom styling
        Backend:
        Python 3.10+
        FastAPI / Flask
        Uvicorn (ASGI server)
        SQLAlchemy (если используется БД)
        Pydantic (валидация данных)
        OpenCV / Pillow (обработка изображений)
        ML:
        PyTorch / TensorFlow
        NumPy
        Pretrained CNN модель для age/gender classification
        База данных (если есть):
        PostgreSQL
        Alembic (миграции)

## 4. Структура репозитория

```
project-root/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── model.py
│   ├── deps.py
│   ├── requirements.txt
│   │
│   ├── database/
│   │   └── db.py
│   │
│   ├── models/
│   │   ├── age_detector/
│   │   ├── face_detector/
│   │   └── gender_detector/
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── history_routes.py
│   │   └── predict_routes.py
│   │
│   ├── schemas/
│   │   ├── prediction.py
│   │   └── user.py
│
├── frontend/
│   ├── index.html
│   ├── eslint_config.js
│   ├── package.json
│   ├── vite.config.js
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   │
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   └── Header.css
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Home.css
│   │   │   ├── Login.jsx
│   │   │   ├── Login.css
│   │   │   ├── Register.jsx
│   │   │   └── Register.css
│   │   │
│   │   └── styles/
│   │       └── global.css
```

## 5. Модель данных + REST API
JSON пример:
```
User {
  id: int,
  email: string,
  password_hash: string
}

Prediction {
  id: int,
  user_id: int,
  age: int,
  gender: string,
  image_path: string,
  created_at: datetime
}
```

REST API
Авторизация
POST /auth/register
POST /auth/login
Предсказание
POST /predict

Request (multipart/form-data):

## 6. Установка и запуск
1. Клонирование репозитория
```
git clone https://github.com/your-repo.git
cd project-root
```
2. Backend
```
cd backend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
```
pip install -r requirements.txt
```
```
uvicorn app.main:app --reload
```

Backend будет доступен:

```
http://localhost:8000
```

3. Frontend будет доступен:
```
cd frontend
npm install
npm run dev
```

Frontend:
```
http://localhost:5173
```
```
-- =========================
-- USERS TABLE
-- =========================

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    password VARCHAR
);

-- =========================
-- PREDICTIONS TABLE
-- =========================

CREATE TABLE public.predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES public.users(id) ON DELETE CASCADE,
    age VARCHAR,
    gender VARCHAR,
    age_confidence DOUBLE PRECISION,
    gender_confidence DOUBLE PRECISION,
    created_at TIMESTAMP
);
```


<img width="1917" height="871" alt="Screenshot 2026-06-12 165734" src="https://github.com/user-attachments/assets/4ba087cf-dd89-40f4-97ee-fed7bef6e6ed" />

<img width="1918" height="871" alt="Screenshot 2026-06-12 165715" src="https://github.com/user-attachments/assets/aafae7a1-17bf-48d1-ab77-7e4271eb16c6" />

<img width="1918" height="868" alt="Screenshot 2026-06-12 165659" src="https://github.com/user-attachments/assets/d1caa7cd-4dba-4cbe-a0fe-a56a0e7c97f5" />
