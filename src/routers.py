from http import HTTPStatus

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from src.models import Album, AlbumUpdate, AlbumUpdateRate

router = APIRouter(prefix='/albums', tags=['albums'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_album(album: Album):
    try:
        album = await album.create()
        return album
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Ranking já em uso'
        )


@router.get('/')
async def get_albums():
    albums = await Album.find_all().to_list()
    return albums


@router.get('/{id}')
async def get_album_id(id: PydanticObjectId):
    album = await Album.get(id)
    if not album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Album not found'
        )
    return album


@router.put('/{id}')
async def update_album(id: PydanticObjectId, album: AlbumUpdate):
    album = {k: v for k, v in album.model_dump().items() if v is not None}
    update_query = {'$set': {field: value for field, value in album.items()}}

    album = await Album.get(id)
    if not album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Album not found'
        )
    await album.update(update_query)
    return album


@router.delete('/{id}')
async def delete_album(id: PydanticObjectId):
    album = await Album.get(id)
    if not album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Album not found'
        )

    await album.delete()
    return {'message': 'Album deleted'}


@router.patch('/{id}/rate')
async def update_rate_album(id: PydanticObjectId, update: AlbumUpdateRate):
    album = await Album.get(id)
    if not album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Album not found'
        )

    album.rate = update.rate
    await album.save()

    return album
