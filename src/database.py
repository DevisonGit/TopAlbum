from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.models import Album
from src.settings import Settings


async def init_db(app: FastAPI):
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    db = client['db_album']

    await init_beanie(database=db, document_models=[Album])

    app.state.mongodb_client = client
    app.state.mongodb = db
