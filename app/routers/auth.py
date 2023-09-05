
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import oauth2, schemas, utils
from app.database import get_db, get_user

router = APIRouter(
    tags=['Authentication']
)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username=username)
    if not user:
        return False
    if not utils.verify(password, user.password):
        return False
    return user

@router.post('/api/v1/jwt/create/', response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пароль или имя пользователя неверно",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth2.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
