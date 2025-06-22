from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.security import get_password_hash
from src.users.models import User

router = APIRouter(prefix='/users', tags=['users'])
templates = Jinja2Templates(directory='templates')


@router.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register-user.html", {"request": request})


@router.post('/')
async def create_user(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    if await User.find_one(User.username == username):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    if await User.find_one(User.email == email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    hashed_password = get_password_hash(password)

    user = User(username=username, email=email, password_hash=hashed_password)
    await user.insert()

    return templates.TemplateResponse(
        'user.html', {'request': request, 'user': user}
    )
