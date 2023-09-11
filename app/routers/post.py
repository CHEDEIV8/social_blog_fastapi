from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
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
def read_post(post: Annotated[models.Post, Depends(get_post)]):
    return post


@router.post('/', response_model=schemas.Post)
def create_post(
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    data: schemas.PostCreate,
    db: Session = Depends(database.get_db),
):
    try:
        return crud.create_post(db, author_id=current_user.id, data=data)
    except crud.GroupDoesNotExist:
        raise utils.not_found('Страница не найдена')


@router.patch('/{post_id}', response_model=schemas.Post)
def partial_update_post(
    post: Annotated[models.Post, Depends(get_post)],
    data: schemas.PostUpdate,
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    db: Session = Depends(database.get_db),
):
    if current_user != post.author:
        raise utils.not_author_error('Нельзя изменить чужой контент')
    try:
        return crud.update_post(db, post=post, data=data)
    except crud.GroupDoesNotExist:
        raise utils.not_found('Страница не найдена')


@router.put('/{post_id}', response_model=schemas.Post)
def update_post(
    post: Annotated[models.Post, Depends(get_post)],
    data: schemas.PostCreate,
    current_user: Annotated[
        schemas.UserInDB, Depends(oauth2.get_current_active_user)
    ],
    db: Session = Depends(database.get_db),
):
    print(request.method)
    if current_user != post.author:
        raise utils.not_author_error('Нельзя изменить чужой контент')

    try:
        return crud.update_post(db, post=post, data=data)
    except crud.GroupDoesNotExist:
        raise utils.not_found('Страница не найдена')


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
