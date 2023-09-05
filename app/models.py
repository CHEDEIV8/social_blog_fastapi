from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    """Модель для пользователей"""

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    

    def __repr__(self) -> str:
        return f'User(id = {self.id!r}, username = {self.username}, email={self.email})'