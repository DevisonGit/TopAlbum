from http import HTTPStatus

import pytest
from bson import ObjectId


@pytest.mark.asyncio
async def test_get_albums(client, album, token):
    album = album.model_dump()

    response = await client.get(
        f'/albums/{album['list_type']}',
        cookies={"access_token": token},
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_albums_empty_list(client):
    response = await client.get('/albums/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_album(client, album):
    response = await client.get(f'/albums/{album.id}')
    album = album.model_dump()
    album['_id'] = str(ObjectId(album['id']))
    album.pop('id')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == album


@pytest.mark.asyncio
async def test_get_album_not_found(client, album):
    response = await client.get(f'/albums/{ObjectId()}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Album not found'}


@pytest.mark.asyncio
async def test_update_album(client, album):
    expected_year = 1988
    expected_title = 'Machado'
    response = await client.put(
        f'/albums/{album.id}',
        json={
            'year': 1988,
            'title': 'Machado',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == expected_title
    assert response.json()['year'] == expected_year


@pytest.mark.asyncio
async def test_update_album_not_found(client, album):
    response = await client.put(
        f'/albums/{ObjectId()}',
        json={'year': 1988, 'title': 'Machado'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Album not found'}


@pytest.mark.asyncio
async def test_delete_album(client, album):
    response = await client.delete(f'/albums/{album.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Album deleted'}


@pytest.mark.asyncio
async def test_delete_album_not_found(client):
    response = await client.delete(f'/albums/{ObjectId()}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Album not found'}


@pytest.mark.asyncio
async def test_update_rate(client, album):
    expected_rate = 9.5
    response = await client.patch(
        f'/albums/{album.id}/rate',
        json={'rate': 9.5},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['rate'] == expected_rate


@pytest.mark.asyncio
async def test_update_rate_not_found(client, album):
    response = await client.patch(
        f'/albums/{ObjectId()}/rate',
        json={'rate': 9.5},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Album not found'}
