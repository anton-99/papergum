from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Papergum API")

# Configure CORS with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Temporary news data for demonstration
MOCK_NEWS = [
    {
        "id": "news-1",
        "headline": "Neue Regelung für Einwegplastik in der Bundesverwaltung",
        "imageUrl": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce",
        "source": "The Guardian US",
        "timestamp": (datetime.now() - timedelta(hours=3)).strftime("%d.%m.%Y %H:%M"),
        "summary": "Die Biden-Administration plant, Einwegplastik, einschließlich Strohhalme, bis 2035 in der gesamten Bundesverwaltung abzuschaffen. Diese Initiative ist Teil eines umfassenderen Umweltschutzprogramms.",
        "relatedSources": [
            {"source": "The Guardian US", "url": "https://theguardian.com/news/1"},
            {"source": "Reuters", "url": "https://reuters.com/news/1"}
        ]
    },
    {
        "id": "news-2",
        "headline": "Ehemaliger NFL-Spieler und Trainer Dick Jauron verstorben",
        "imageUrl": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2",
        "source": "ESPN",
        "timestamp": (datetime.now() - timedelta(hours=2)).strftime("%d.%m.%Y %H:%M"),
        "summary": "Dick Jauron, ein ehemaliger NFL-Spieler und Trainer, ist am Samstag im Alter von 74 Jahren verstorben. Jauron war ein zweifacher Sportstar an der Yale University und hatte eine bemerkenswerte Karriere in der NFL.",
        "relatedSources": [
            {"source": "ESPN", "url": "https://espn.com/news/1"},
            {"source": "NFL", "url": "https://nfl.com/news/1"}
        ]
    }
]

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

@app.get("/")
async def read_root():
    return {"message": "Willkommen zur Papergum API"}

@app.get("/api/news")
async def get_news():
    logger.info("Fetching all news items")
    return MOCK_NEWS

@app.get("/api/news/{news_id}")
async def get_news_detail(news_id: str):
    logger.info(f"Fetching news item with id: {news_id}")
    news_item = next((item for item in MOCK_NEWS if item["id"] == news_id), None)
    
    if news_item is None:
        logger.warning(f"News item not found: {news_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Artikel mit ID {news_id} wurde nicht gefunden"
        )
    
    logger.info(f"Found news item: {news_item['headline']}")
    return news_item
