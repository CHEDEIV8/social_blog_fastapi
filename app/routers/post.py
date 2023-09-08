from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import crud, database, models, oauth2, schemas, utils

router = APIRouter(prefix='/posts', tags=['Posts'])


def get_post(post_id: int, db: Session = Depends(database.get_db)):
    post = crud.get_post(db, post_id=post_id)
    if not post:
        raise utils.not_found('Страница не найдена')
    return post


@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(database.get_db)):
    return crud.get_posts(db)


@router.get('/{post_id}', response_model=schemas.Post)
def read_group(post: Annotated[models.Post, Depends(get_post)]):
    return post


@router.post('/', response_model=schemas.Post)
def create_post(
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    data: schemas.PostCreate,
    db: Session = Depends(database.get_db),
):
    if data.group:
        group = crud.get_group(db, group_id=data.group)
        if not group:
            raise utils.not_found('Страница не найдена')
    else:
        group = None

    return crud.create_post(
        db,
        author_id=current_user.id,
        text=data.text,
        image=data.image,
        group_id=group.id if group else None,
    )


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    post: Annotated[models.Post, Depends(get_post)],
    db: Session = Depends(database.get_db),
):
    if current_user != post.author:
        raise utils.not_author_error('Нельзя изменить чужой контент')
    crud.delete_post(db, post=post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
