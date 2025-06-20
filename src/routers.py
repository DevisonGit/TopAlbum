from http import HTTPStatus

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pymongo.errors import DuplicateKeyError
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from src.models import Album, AlbumUpdate, AlbumUpdateRate, AlbumForm

router = APIRouter(prefix='/albums', tags=['albums'])
templates_teste = Jinja2Templates(directory='templates')


@router.get("/criar", response_class=HTMLResponse)
async def form_criar(request: Request):
    return templates_teste.TemplateResponse("create.html", {"request": request})


@router.post("/criar")
async def criar_album(form: AlbumForm = Depends(AlbumForm.as_form)):
    album = Album(**form.model_dump())
    await album.insert()
    return RedirectResponse("/albums/", status_code=302)


@router.get('/', response_class=HTMLResponse)
async def listar_tarefas(request: Request):
    albums = await Album.find_all().sort('ranking').to_list()
    return templates_teste.TemplateResponse("index.html", {"request": request, "albums": albums})




# @router.post('/', status_code=HTTPStatus.CREATED)
# async def create_album(album: Album):
#     try:
#         album = await album.create()
#         return album
#     except DuplicateKeyError:
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST, detail='Ranking in use'
#         )


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
    return JSONResponse(content={"ok": True})


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
