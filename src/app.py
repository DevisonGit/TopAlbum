from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.database import init_db
from src.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    await init_db(app)
    yield
    client = getattr(app.state, 'mongodb_client', None)
    if client:
        client.close()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory='templates')


app.include_router(router)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
