from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db, get_user

from .. import oauth2, schemas, utils

router = APIRouter(tags=['Authentication'])


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username=username)
    if not user:
        return False
    if not utils.verify(password, user.password):
        return False
    return user


@router.post('/jwt/create', response_model=schemas.Tokens)
async def login_for_jwt_token(
    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    token_data: schemas.TokenCreate,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, **token_data.model_dump())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пароль или имя пользователя неверно',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    data = {'sub': user.username}
    refresh_token = oauth2.create_refresh_token(data=data)
    access_token = oauth2.create_access_token(data=data)
    return {'refresh': refresh_token, 'access': access_token}


@router.post('/jwt/refresh', response_model=schemas.AccessTokens)
async def refresh_access_token(
    token: schemas.RefreshTokens,
):
    refresh_token = token.refresh
    token_data = oauth2.verify_jwt_token(refresh_token)
    data = {'sub': token_data.username}
    return {'access': oauth2.create_access_token(data=data)}


@router.post('/jwt/verify')
async def verify_token(
    token: schemas.Token,
):
    oauth2.verify_jwt_token(token.token)
    return Response(status_code=status.HTTP_200_OK)
