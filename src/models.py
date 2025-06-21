from typing import Literal, Optional

import pymongo
from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from pymongo import IndexModel


class Album(Document):
    title: str
    artist: str
    ranking: int
    year: int
    media: float | None = None
    list_type: Literal[
        'brasil', 'rollingstone-internacional', 'rollingstone-brasil'
    ]

    class Settings:
        name = 'albums'
        indexes = [
            'ranking',
            [
                ('ranking', pymongo.ASCENDING),
                ('list_type', pymongo.DESCENDING),
            ],
            IndexModel(
                [('list_type', pymongo.DESCENDING)],
                name='test_string_index_DESCENDING',
            ),
        ]

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'name albums',
                'artist': 'name artist',
                'ranking': 1,
                'year': 2025,
            }
        }


class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    year: Optional[int] = None

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'name albums',
                'artist': 'name artist',
                'ranking': 1,
                'year': 2025,
            }
        }


class AlbumUserRate(Document):
    user_id: str
    album_id: PydanticObjectId
    rate: float

    class Settings:
        name = 'user_album_ratings'
