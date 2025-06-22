from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from src.albums.routers import router
from src.auth.routers import router as router_auth
from src.database import init_db
from src.security import get_current_user_from_cookie
from src.templates import templates
from src.users.router import router as router_user


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    await init_db(app)
    yield
    client = getattr(app.state, 'mongodb_client', None)
    if client:
        client.close()


app = FastAPI(lifespan=lifespan)


app.include_router(router)
app.include_router(router_user)
app.include_router(router_auth)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def home(
    request: Request, user_id: str = Depends(get_current_user_from_cookie)
):
    is_authenticated = user_id is not None
    return templates.TemplateResponse(
        'home.html', {'request': request, 'is_authenticated': is_authenticated}
    )


@app.get('/favicon.ico')
async def favicon():
    return Response(status_code=204)
