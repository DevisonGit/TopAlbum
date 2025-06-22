from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse

from src.security import verify_password, create_access_token
from src.users.models import User
from src.templates import templates


router = APIRouter(prefix='/login', tags=['auth'])


@router.get("/", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post('/')
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
