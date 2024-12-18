from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate, UserModel
from auth import (
    get_user,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_moderator_user,
    get_current_admin_user,
)
from database import get_db


app = FastAPI()

# Залежність для отримання сесії бази даних


# Маршрут для реєстрації користувача
@app.post("/register", response_model=UserModel)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Користувач з таким іменем вже існує"
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username, hashed_password=hashed_password, role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Маршрут для отримання токена
@app.post("/token")
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильне ім'я користувача або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Перший маршрут - доступний для всіх
@app.get("/public")
def read_public():
    return {"message": "Це публічний маршрут, доступний для всіх"}


# Другий маршрут - для модераторів та адміністраторів
@app.get("/moderator")
def read_moderator(
    current_user: User = Depends(get_current_moderator_user),
):
    return {
        "message": f"Вітаємо, {current_user.username}! Це маршрут для модераторів та адміністраторів"
    }


# Третій маршрут - тільки для адміністраторів
@app.get("/admin")
def read_admin(current_user: User = Depends(get_current_admin_user)):
    return {"message": f"Вітаємо, {current_user.username}! Це адміністративний маршрут"}
