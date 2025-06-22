from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, DecodeError, ExpiredSignatureError
from pwdlib import PasswordHash

from src.settings import Settings
from src.users.models import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = await  User.find_one(User.username == subject_email)

    if not user:
        raise credentials_exception

    return user


def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        username = payload.get("sub")
        return username
    except ExpiredSignatureError:
        return None
    except DecodeError:
        raise None
