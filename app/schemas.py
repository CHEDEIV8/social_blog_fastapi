from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class User(UserBase):
    is_active: bool


class UserCreate(UserBase):
    password: str


class UserInDB(User):
    id: int
    password: str


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
    user: str
    following: str


class FollowCreate(BaseModel):
    following: str
