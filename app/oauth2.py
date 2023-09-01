from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from . import main, schemas, config
from .database import engine

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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception 
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = main.get_user(main.fake_users_db, username=token.username)
    if user is None:
        raise credentials_exception
    return user