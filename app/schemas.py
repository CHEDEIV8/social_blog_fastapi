from datetime import datetime
from .utils import save_image

from pydantic import AliasPath, BaseModel, EmailStr, Field, field_validator

MIN_LENGTH_USERNAME = 3
MAX_LENGTH_PASSWORD = 8


class UserBase(BaseModel):
    username: str = Field(min_length=MIN_LENGTH_USERNAME)
    email: EmailStr


class User(UserBase):
    is_active: bool


class UserCreate(UserBase):
    password: str = Field(max_length=MAX_LENGTH_PASSWORD)


class UserInDB(User):
    id: int
    password: str = Field(max_length=MAX_LENGTH_PASSWORD)


class RefreshTokens(BaseModel):
    refresh: str


class AccessTokens(BaseModel):
    access: str


class Tokens(RefreshTokens, AccessTokens):
    pass


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    username: str


class TokenCreate(BaseModel):
    username: str
    password: str


class ErrorMessage(BaseModel):
    detail: str


class Group(BaseModel):
    id: int
    title: str
    slug: str
    description: str


class Follow(BaseModel):
    user: str = Field(validation_alias=AliasPath('user', 'username'))
    following: str = Field(validation_alias=AliasPath('following', 'username'))


class FollowCreate(BaseModel):
    following: str


class Post(BaseModel):
    id: int
    author: str = Field(validation_alias=AliasPath('author', 'username'))
    text: str
    pub_date: datetime
    image: str | None
    group: int | None = Field(
        default=None, validation_alias=AliasPath('group', 'id')
    )

    @field_validator('image')
    @classmethod
    def relative_url_for_image(cls, value: str | None):
        if value:
            return '/media/' + value
        return value


class PostCreate(BaseModel):
    text: str
    image: str | None = None
    group: int | None = None

    @field_validator('image')
    @classmethod
    def save_image(cls, value: str | None):
        if not value:
            return value
        if not value.startswith('data:image'):
            raise ValueError('Картинка должна начинаться с data:image')
        try:
            filename = save_image(value)
        except Exception as e:
            raise ValueError(f'Ошибка при сохранении файла {e}')
        return filename
        


class PostUpdate(PostCreate):
    text: str | None = None

    @field_validator('text')
    @classmethod
    def name_cannot_be_null(cls, value: str | None):
        if value is None:
            raise ValueError('поле text не может быть пустым.')
        return value


class Comment(BaseModel):
    id: int
    author: str = Field(validation_alias=AliasPath('author', 'username'))
    text: str
    created: datetime
    post: int = Field(validation_alias=AliasPath('post', 'id'))


class CommentCreate(BaseModel):
    text: str
