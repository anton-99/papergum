from pydantic import BaseModel
from typing import List

class RelatedSource(BaseModel):
    source: str
    url: str

class NewsDetail(BaseModel):
    id: str
    headline: str
    imageUrl: str
    source: str
    timestamp: str
    summary: str
    relatedSources: List[RelatedSource]
