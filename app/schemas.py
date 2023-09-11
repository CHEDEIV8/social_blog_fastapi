from datetime import datetime

from pydantic import AliasPath, BaseModel, EmailStr, Field, validator

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


class PostCreate(BaseModel):
    text: str
    image: str | None = None
    group: int | None = None


class PostUpdate(PostCreate):
    text: str | None = None
    @validator('text')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('поле text не может быть пустым.')
        return value
