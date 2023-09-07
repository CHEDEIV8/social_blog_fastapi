from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# SQLALCHEMY_DTABASE_URL = 'postgresql://<username>:<password>@<ip: adress/hostname>/<data_base_name>'
SQLALCHEMY_DTABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DTABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
