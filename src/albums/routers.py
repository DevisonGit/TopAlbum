from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse

from src.albums.services import AlbumService
from src.security import get_current_user_from_cookie
from src.share.models import FilterPage
from src.templates import templates

router = APIRouter(prefix='/albums', tags=['albums'])
UserId = Annotated[str, Depends(get_current_user_from_cookie)]


@router.get('/{list_type}', response_class=HTMLResponse)
async def list_albums(
    list_type: str,
    request: Request,
    user_id: UserId,
    page: int = Query(1),
    limit: int = Query(20),
):
    filter_page = FilterPage(page=page, limit=limit)
    service = AlbumService(filter_page, user_id, list_type)
    albums_ratings = await service.get_albums()
    albums_ratings.update({'request': request})

    return templates.TemplateResponse('albums/list.html', albums_ratings)


@router.get('/id/{album_id}')
async def get_album_id(
    album_id: PydanticObjectId,
    request: Request,
    user_id: str = Depends(get_current_user_from_cookie),
):
    service = AlbumService(user_id=user_id)
    album = await service.get_album(album_id)
    album.update({'request': request})

    return templates.TemplateResponse('albums/album.html', album)


@router.post('/{album_id}/rate')
async def update_rate_album(
    album_id: PydanticObjectId,
    request: Request,
    rate: float = Form(...),
    user_id: str = Depends(get_current_user_from_cookie),
):
    service = AlbumService(user_id=user_id)
    album = await service.update_rate(album_id, rate)
    album.update({'request': request})
    return templates.TemplateResponse('albums/album.html', album)
