from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, database, oauth2, schemas, utils

router = APIRouter(prefix='/follow', tags=['Follow'])

FOLLOW_NOT_FOUND = {'following': ['Пользователь не найден']}
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
    return follows


# [
#         {
#             'user': follow.user.username,
#             'following': follow.following.username,
#         }
#         for follow in follows
#     ]


@router.post('/', response_model=schemas.Follow)
def read_follow(
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    data: schemas.FollowCreate,
    db: Session = Depends(database.get_db),
):
    following_user = crud.get_user(db, username=data.following)
    if not following_user:
        raise utils.validation_error(FOLLOW_NOT_FOUND)
    if current_user == following_user:
        raise utils.validation_error(CANT_FOLLOW_SELF)
    try:
        follow = crud.create_follow(
            db,
            user_id=current_user.id,
            following_id=following_user.id,
        )
    except crud.FollowExists:
        raise utils.validation_error(FOLLOW_ALREDY_EXIST)

    return follow
