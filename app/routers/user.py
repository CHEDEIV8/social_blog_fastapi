from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import database, oauth2, schemas

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/',
             response_model=schemas.User,
             status_code=status.HTTP_201_CREATED)
def create_users(user: schemas.UserCreate,
                 db: Session = Depends(get_db)):
    try:
        return database.create_user(db, user)
    except database.UserExists:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пользователь с таким email или username уже существует",
    )


@router.get("/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_active_user)]
):
    return current_user

@router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]