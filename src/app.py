from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import init_db
from src.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    yield
    client = getattr(app.state, 'mongodb_client', None)
    if client:
        client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
