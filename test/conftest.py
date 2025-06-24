import factory
import pytest
import pytest_asyncio
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

from src.albums.models import Album
from src.app import app
from src.security import get_password_hash
from src.users.models import User


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album

    title = factory.Faker('sentence', nb_words=3)
    artist = factory.Faker('sentence', nb_words=3)
    ranking = factory.Sequence(lambda n: n)
    year = factory.Sequence(lambda n: n + 1990)
    rate = None
    list_type = 'brasil'


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password_hash = factory.LazyAttribute(
        lambda obj: f'<PASSWORD>{obj.username}')


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


@pytest_asyncio.fixture
async def album(test_app):
    album = AlbumFactory.build()

    await album.insert()

    return album


@pytest_asyncio.fixture(autouse=True)
async def cleanup_database(test_app):
    for collection in await test_app.state.mongodb.list_collection_names():
        await test_app.state.mongodb[collection].delete_many({})


@pytest_asyncio.fixture
async def user(test_app):
    password = 'testtest'
    user_data = UserFactory().build()
    user_data.password_hash = get_password_hash(password)
    user = user_data.model_dump()

    result = await test_app.mongodb.users.insert_one(user)
    user['_id'] = str(result.inserted_id)
    user['clean_password'] = password

    return user


@pytest_asyncio.fixture
async def token(client, user):
    response = await client.post(
        '/auth/token',
        data={'username': user['email'], 'password': user['clean_password']},
    )
    return response.json()['access_token']
