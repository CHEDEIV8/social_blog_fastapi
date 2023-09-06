from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import database, oauth2, schemas

router = APIRouter(prefix='/users', tags=['Users'])


@router.post(
    '/',
    response_model=schemas.User,
    responses={
        400: {
            'description': 'Пользователь с таким email или username уже существует',
            'model': schemas.ErrorMessage,
        },
    },
    status_code=status.HTTP_201_CREATED,
)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return database.create_user(db, user)
    except database.UserExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким email или username уже существует',
        )


@router.get("/me", response_model=schemas.User)
async def read_me(
    current_user: Annotated[
        schemas.User, Depends(oauth2.get_current_active_user)
    ]
):
    return current_user
