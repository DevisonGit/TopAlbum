from math import ceil

from beanie import PydanticObjectId

from src.albums.models import Album, AlbumUserRate
from src.share.models import FilterPage


class AlbumService:
    def __init__(
        self,
        _filter: FilterPage = None,
        user_id: str = None,
        list_type: str = None,
    ):
        self._filter = _filter
        self.user_id = user_id
        self.list_type = list_type

    async def get_albums(self) -> dict:
        is_authenticated = self.user_id is not None
        total_pages = await self.get_total_pages()
        list_type_title = self.get_list_type_title()
        albums_data = await self.get_albums_ratings()

        albums_dict = {
            'albums': albums_data,
            'lista': list_type_title,
            'is_authenticated': is_authenticated,
            'total_pages': total_pages,
            'page': self._filter.page,
            'list_type': self.list_type,
        }
        return albums_dict

    async def get_total_pages(self) -> int:
        total_albums = await Album.find(
            Album.list_type == self.list_type
        ).count()
        total_pages = ceil(total_albums / self._filter.limit)
        return total_pages

    def get_list_type_title(self) -> str:
        titles = {
            'brasil': '500 Álbuns Mais Importantes do Brasil',
            'rollingstone-internacional': '500 Álbuns da '
            'Rolling Stone (Internacional)',
            'rollingstone-brasil': '100 Álbuns da Rolling Stone Brasil',
        }
        return titles.get(self.list_type)

    async def get_albums_ratings(self) -> list:
        albums_data = []
        skip = (self._filter.page - 1) * self._filter.limit
        albums = (
            await Album.find(Album.list_type == self.list_type)
            .skip(skip)
            .limit(self._filter.limit)
            .sort('-ranking')
            .to_list()
        )
        ratings = await AlbumUserRate.find(
            AlbumUserRate.user_id == self.user_id
        ).to_list()
        ratings_dict = {r.album_id: r.rate for r in ratings}

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
        return albums_data

    async def get_album(self, album_id: PydanticObjectId) -> dict:
        album = await Album.get(album_id)
        is_authenticated = self.user_id is not None
        if not album:
            return {'album': album}
        rating = await AlbumUserRate.find_one({
            'user_id': self.user_id,
            'album_id': album_id,
        })
        user_rate = rating.rate if rating else None
        return {'album': album, 'rate': user_rate, 'is_authenticated': is_authenticated,}

    async def update_rate(
        self, album_id: PydanticObjectId, rate: float
    ) -> dict:
        is_authenticated = self.user_id is not None
        album = await Album.get(album_id)
        if not album:
            return {'album': album}
        rating = await AlbumUserRate.find_one({
            'user_id': self.user_id,
            'album_id': album_id,
        })
        if rating:
            rating.rate = rate
            await rating.save()
        else:
            await AlbumUserRate(
                user_id=self.user_id, album_id=album_id, rate=rate
            ).insert()
        await self.update_media(album)
        return {'album': album, 'rate': rate, 'is_authenticated': is_authenticated,}

    @staticmethod
    async def update_media(album):
        ratings = await AlbumUserRate.find(
            AlbumUserRate.album_id == album.id
        ).to_list()
        media = (
            round(sum(r.rate for r in ratings) / len(ratings), 2)
            if ratings
            else None
        )
        album.media = media
        await album.save()
