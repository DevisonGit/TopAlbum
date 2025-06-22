from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.security import get_password_hash
from src.users.models import User, UserPublic

router = APIRouter(prefix='/users', tags=['users'])
templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse(
        'users/register.html', {'request': request}
    )


@router.post('/')
async def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    if await User.find_one(User.username == username):
        return templates.TemplateResponse(
            'users/register.html',
            {'request': request, 'error': 'Usuário já existe'},
        )
    if await User.find_one(User.email == email):
        return templates.TemplateResponse(
            'users/register.html',
            {'request': request, 'error': 'E-mail já cadastrado'},
        )

    hashed_password = get_password_hash(password)

    user = User(username=username, email=email, password_hash=hashed_password)
    await user.insert()

    user_public = UserPublic(**user.model_dump())

    return templates.TemplateResponse(
        'users/user.html', {'request': request, 'user': user_public}
    )
