from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse

from src.security import verify_password, create_access_token
from src.users.models import User
from src.templates import templates


router = APIRouter(tags=['auth'])


@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post('/login')
async def login_for_access_token(
request: Request,
        form_data: OAuth2PasswordRequestForm = Depends()

):
    user = await User.find_one(User.username == form_data.username)
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "Usuário ou senha inválidos."
            }
        )

    if not verify_password(form_data.password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "Usuário ou senha inválidos."
            }
        )
    access_token = create_access_token(data={'sub': user.email})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        path="/"
    )
    response.set_cookie(
        key="is_authenticated",
        value=user.username,
        httponly=True,
        path="/"
    )

    return response


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")  # ou "user_id", se for esse o nome do cookie
    return response
