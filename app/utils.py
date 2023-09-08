from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    """Функция для хэширования пароля"""

    return pwd_context.hash(password)


def verify(password, hashed_password):
    """Функция проверки пароля при входе в систему"""

    return pwd_context.verify(password, hashed_password)


def not_found(message: str):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


def validation_error(message: dict):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


def not_author_error(message: str):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message,
    )
