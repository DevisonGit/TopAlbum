from beanie import Document, Indexed
from pydantic import EmailStr


class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    password_hash: str

    class Settings:
        name = 'users'
