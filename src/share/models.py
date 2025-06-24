from typing import Optional

from pydantic import BaseModel


class FilterPage(BaseModel):
    page: Optional[int] = 1
    limit: Optional[int] = 20
