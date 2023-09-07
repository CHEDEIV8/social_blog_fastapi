from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, database, oauth2, schemas, utils

router = APIRouter(prefix='/follow', tags=['Follow'])

FOLLOW_NOT_FOUND  = {'following': ['Пользователь не найден']}
CANT_FOLLOW_SELF = {'following': ['Нельзя подписаться на самого себя']}
FOLLOW_ALREDY_EXIST = {'following': ['Подписка уже существует']}

@router.get('/', response_model=list[schemas.Follow])
def read_follows(
    current_user: Annotated[
        schemas.User, Depends(oauth2.get_current_active_user)
    ],
    db: Session = Depends(database.get_db),
):
    follows = crud.get_follows(db, username=current_user.username)
    return [
        {
            'user': follow.user.username,
            'following': follow.following.username,
        }
        for follow in follows
    ]


@router.post('/', response_model=schemas.Follow)
def read_follow(
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    follow: schemas.FollowCreate,
    db: Session = Depends(database.get_db),
):
    following = crud.get_user(db, username=follow.following)
    if not following:
        raise utils.validation_error(FOLLOW_NOT_FOUND)
    if current_user == following:
        raise utils.validation_error(CANT_FOLLOW_SELF)
    try:
        crud.create_follow(
            db,
            user_id=current_user.id,
            following_id=following.id,
        )
    except crud.FollowExists:
        raise utils.validation_error(FOLLOW_ALREDY_EXIST)

    return {
        'user': current_user.username,
        'following': following.username,
    }
