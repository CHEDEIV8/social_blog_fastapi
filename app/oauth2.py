from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import schemas, config, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/jwt/create/')

SECRET_KEY = config.settings.secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    """Функция создает токен доступа"""
    
    to_encode = data.copy()
    # получаем время хранения токена
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # добавляем в словарь и потом его передаем
    to_encode.update({'exp': expire})
    # кодируем данные для получения jwt токена
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # type: ignore
        if username is None:
            raise credentials_exception 
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    return token_data

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = database.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[schemas.UserInDB, Depends(get_current_user)]
):
    if current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь неактивен")
    return current_user