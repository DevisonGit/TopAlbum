import factory
import pytest
import pytest_asyncio
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

from src.app import app
from src.models import Album


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album

    title = factory.Faker('sentence', nb_words=3)
    artist = factory.Faker('sentence', nb_words=3)
    ranking = factory.Sequence(lambda n: n)
    year = factory.Sequence(lambda n: n + 1990)
    rate = None


@pytest.fixture(scope='session')
def mongo_container():
    with MongoDbContainer('mongo:latest') as mongo:
        yield mongo


@pytest_asyncio.fixture
async def test_app(mongo_container):
    mongo_uri = mongo_container.get_connection_url()
    db_name = 'test_db_album'

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]

    await init_beanie(database=db, document_models=[Album])

    app.state.mongodb_client = client
    app.state.mongodb = db

    yield app

    client.close()


@pytest_asyncio.fixture
async def client(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac
