from fastapi import HTTPException, Query, status
from fastapi_pagination.links import LimitOffsetPage
from passlib.context import CryptContext
import base64
import uuid
from .config import BASE_DIR

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


Page = LimitOffsetPage.with_custom_options(limit=Query(10, ge=1, le=500))

def save_image(value):
    img_format, img_str = value.split(';base64,')
    ext = img_format.split('/')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    img_data = base64.b64decode(img_str)
    with open(BASE_DIR / 'media' / filename, 'wb') as f:
        f.write(img_data)
        # raise ValueError(f'Ошибка при сохранении файла {e}')
    return filename