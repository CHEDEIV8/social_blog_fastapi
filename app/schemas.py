from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class User(UserBase):
    is_active: bool


class UserCreate(UserBase):
    password: str


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str