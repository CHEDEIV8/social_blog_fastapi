from sqlalchemy import select, update
from sqlalchemy.orm import Session

from . import models, schemas, utils


def get_user(db: Session, username: str):
    return db.scalar(
        select(models.User).where(models.User.username == username)
    )


class UserExists(Exception):
    pass


class FollowExists(Exception):
    pass


class GroupDoesNotExist(Exception):
    pass


def create_user(db: Session, user: schemas.UserCreate):
    stmt = select(models.User).where(
        (models.User.username == user.username)
        | (models.User.email == user.email)
    )
    if db.execute(stmt).first():
        raise UserExists
    hashed_password = utils.hash(user.password)
    user_data = user.model_dump() | {'password': hashed_password}
    db_user = models.User(**user_data)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_groups(db: Session):
    return db.scalars(select(models.Group)).all()


def get_group(db: Session, group_id):
    return db.scalar(select(models.Group).where(models.Group.id == group_id))


def get_follows(db: Session, username: str):
    return db.scalars(
        select(models.Follow)
        .join(models.User, models.Follow.user_id == models.User.id)
        .where(models.User.username == username)
    ).all()


def create_follow(db: Session, following_id: int, user_id: int):
    stmt = select(models.Follow).where(
        (models.Follow.user_id == user_id),
        (models.Follow.following_id == following_id),
    )
    if db.execute(stmt).first():
        raise FollowExists
    db_follow = models.Follow(user_id=user_id, following_id=following_id)

    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)

    return db_follow


def get_posts(db: Session):
    return db.scalars(select(models.Post)).all()


def get_post(db: Session, post_id):
    return db.scalar(select(models.Post).where(models.Post.id == post_id))

def create_post(db: Session, author_id: int, data: schemas.PostCreate):
    if data.group and not get_group(db, group_id=data.group):
        raise GroupDoesNotExist
    db_post = models.Post(
        **data.model_dump(exclude={'group'}),
        group_id=data.group,
        author_id=author_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post: models.Post, data: schemas.PostUpdate):
    if data.group and not get_group(db, group_id=data.group):
        raise GroupDoesNotExist
    update_data = data.model_dump(exclude_unset=True)
    if 'group' in update_data:
        update_data['group_id'] = update_data.pop('group')

    for field, value in update_data.items():
        setattr(post, field, value)

    db.add(post)   
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: models.Post):
    db.delete(post)
    db.commit()
