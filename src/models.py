from typing import Optional

from beanie import Document, Indexed
from fastapi import Form
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


class AlbumForm(BaseModel):
    title: str
    artist: str
    ranking: int
    year: int
    rate: float | None = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        artist: str = Form(...),
        ranking: int = Form(...),
        year: int = Form(...),
        rate: float | None = Form(None),
    ):
        return cls(
            title=title,
            artist=artist,
            ranking=ranking,
            year=year,
            rate=rate,
        )
