from http import HTTPStatus

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.app import app


@pytest.mark.anyio
async def test_lifespan_initializes_mongodb(fastapi_app: FastAPI):
    async with LifespanManager(fastapi_app):
        async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url='http://test'
        ) as client:
            # aqui o init_db já foi chamado
            # você pode inserir um documento e verificar que funciona
            resp = await client.get('/albums/')
            assert resp.status_code == HTTPStatus.OK


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}
