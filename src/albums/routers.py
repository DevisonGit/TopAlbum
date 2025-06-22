from http import HTTPStatus

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from pymongo.errors import DuplicateKeyError

from src.albums.models import Album, AlbumUserRate
from src.security import get_current_user_from_cookie
from src.templates import templates


router = APIRouter(prefix='/albums', tags=['albums'])


@router.get('/{list_type}', response_class=HTMLResponse)
async def list_albums(
    list_type: str, request: Request, user_id: str = Depends(get_current_user_from_cookie)
):
    albums = (
        await Album.find(Album.list_type == list_type)
        .sort('-ranking')
        .to_list()
    )
    ratings = await AlbumUserRate.find(
        AlbumUserRate.user_id == user_id
    ).to_list()
    ratings_dict = {r.album_id: r.rate for r in ratings}

    albums_data = []

    for album in albums:
        albums_data.append({
            'id': str(album.id),
            'ranking': album.ranking,
            'title': album.title,
            'artist': album.artist,
            'year': album.year,
            'media': album.media,
            'rate': ratings_dict.get(album.id),
        })

    titles = {
        'brasil': '500 Álbuns Mais Importantes do Brasil',
        'rollingstone-internacional': '500 Álbuns da '
        'Rolling Stone (Internacional)',
        'rollingstone-brasil': '100 Álbuns da Rolling Stone Brasil',
    }
    list_type = titles.get(list_type)

    return templates.TemplateResponse(
        'albums/list.html',
        {'request': request, 'albums': albums_data, 'lista': list_type},
    )


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_album(album: Album):
    try:
        album = await album.create()
        return album
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Ranking in use'
        )


@router.get('/id/{id}')
async def get_album_id(
    id: PydanticObjectId,
    request: Request,
    user_id: str = Depends(get_current_user_from_cookie),
):
    album = await Album.get(id)
    if not album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Album not found'
        )
    rating = await AlbumUserRate.find_one({'user_id': user_id, 'album_id': id})
    user_rate = rating.rate if rating else None

    return templates.TemplateResponse(
        'albums/album.html', {'request': request, 'album': album, 'rate': user_rate}
    )


@router.post('/{id}/rate')
async def update_rate_album(
    id: PydanticObjectId,
    request: Request,
    rate: float = Form(...),
    user_id: str = Depends(get_current_user_from_cookie),
):
    album = await Album.get(id)
    if not album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Album not found'
        )
    rating = await AlbumUserRate.find_one({'user_id': user_id, 'album_id': id})

    if rating:
        rating.rate = rate
        await rating.save()
    else:
        await AlbumUserRate(user_id=user_id, album_id=id, rate=rate).insert()
    await update_media(album)
    return templates.TemplateResponse(
        'albums/album.html', {'request': request, 'album': album, 'rate': rate}
    )


async def update_media(album):
    ratings = await AlbumUserRate.find(
        AlbumUserRate.album_id == album.id
    ).to_list()
    media = (
        round(sum(r.rate for r in ratings) / len(ratings), 2)
        if ratings
        else None
    )

    # Atualiza o campo no álbum
    album.media = media
    await album.save()
