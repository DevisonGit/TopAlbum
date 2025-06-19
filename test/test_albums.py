from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_album(client):
    response = await client.post(
        '/albums/',
        json={
            'artist': 'Test artist',
            'year': 2025,
            'ranking': 1,
            'title': 'Test title!',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
