from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth.models import Token
from src.security import verify_password, create_access_token
from src.users.models import User

router = APIRouter(prefix='/auth', tags=['auth'])
templates = Jinja2Templates(directory='templates')


@router.post('/token')
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await User.find_one(User.username == form_data.username)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        path="/"
    )

    return response


@router.get("/token", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})