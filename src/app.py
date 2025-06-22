from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.database import init_db
from src.albums.routers import router
from src.users.router import router as router_user
from src.auth.routers import router as router_auth
from src.templates import templates


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
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
