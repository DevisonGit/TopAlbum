from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel


class Album(Document):
    title: str
    artist: str
    ranking: Indexed(int, unique=True)
    year: int
    rate: float | None = None

    class Settings:
        name = 'albums'

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
    ranking: Optional[int] = None
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


class AlbumUpdateRate(BaseModel):
    rate: float
