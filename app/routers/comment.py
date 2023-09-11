from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.routers.post import get_post

from .. import crud, database, models, oauth2, schemas, utils

router = APIRouter(prefix='/posts/{post_id}/comments', tags=['Posts'])


def get_comment(
    comment_id: int,
    post: Annotated[models.Post, Depends(get_post)],
    db: Session = Depends(database.get_db),
):
    comment = crud.get_comment(db, comment_id=comment_id, post=post)
    if not comment:
        raise utils.not_found('Страница не найдена')
    return comment


@router.get("/", response_model=list[schemas.Comment])
def read_comments(post: Annotated[models.Post, Depends(get_post)]):
    return crud.get_comments(post)


@router.get('/{comment_id}', response_model=schemas.Comment)
def read_comment(comment: Annotated[models.Comment, Depends(get_comment)]):
    return comment


@router.post('/', response_model=schemas.Comment)
def create_comment(
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    post: Annotated[models.Post, Depends(get_post)],
    data: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
):
    return crud.create_comment(db, data, post, author_id=current_user.id)


@router.put('/{comment_id}', response_model=schemas.Comment)
@router.patch('/{comment_id}', response_model=schemas.Comment)
def update_comment(
    post: Annotated[models.Post, Depends(get_comment)],
    data: schemas.PostUpdate,
    comment: Annotated[models.Comment, Depends(get_comment)],
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    db: Session = Depends(database.get_db),
):
    if current_user != comment.author:
        raise utils.not_author_error('Нельзя изменить чужой контент')
    return crud.update_comment(db, comment=comment, data=data)


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    comment: Annotated[models.Comment, Depends(get_comment)],
    post: Annotated[models.Post, Depends(get_post)],
    db: Session = Depends(database.get_db),
):
    if current_user != comment.author:
        raise utils.not_author_error('Нельзя изменить чужой контент')
    crud.delete_comment(db, comment=comment)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
