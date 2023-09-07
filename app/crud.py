from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas, utils


def get_user(db: Session, username: str):
    return db.scalar(
        select(models.User).where(models.User.username == username)
    )


class UserExists(Exception):
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
