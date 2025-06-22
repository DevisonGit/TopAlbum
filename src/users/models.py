from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr


class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    password_hash: str

    class Settings:
        name = 'users'


class UserPublic(BaseModel):
    username: str
    email: EmailStr
