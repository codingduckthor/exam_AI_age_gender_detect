AI Age & Gender Detection Project
1. Описание проекта + функциональные возможности

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

2. Архитектура проекта

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

3. Использованные технологии
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

4. Структура репозитория

```
project-root/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── ml/
│   │   └── database/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── README.md
```

5. Модель данных + REST API
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

6. Установка и запуск
1. Клонирование репозитория
git clone https://github.com/your-repo.git
cd project-root
2. Backend
cd backend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
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

3. Frontend
```
cd frontend
npm install
npm run dev
```

Frontend:
```
http://localhost:5173
```
