from sqlalchemy import create_engine, select

from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from . import models, schemas, utils

# SQLALCHEMY_DTABASE_URL = 'postgresql://<username>:<password>@<ip: adress/hostname>/<data_base_name>'
SQLALCHEMY_DTABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DTABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserExists(Exception):
    pass


# Dependency
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: Session, username: str):
    return db.scalar(select(models.User).where(models.User.username == username))


def create_user(db: Session, user: schemas.UserCreate):
    stmt = select(models.User).where(
        (models.User.username == user.username) | (models.User.email == user.email)
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