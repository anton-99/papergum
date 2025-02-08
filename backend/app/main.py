from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime, timedelta
import logging
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import news

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Papergum API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the news router
app.include_router(news.router, tags=["news"])

# Aktuelle Nachrichten
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
    },
    {
        "id": "news-3",
        "headline": "Durchbruch in der Quantencomputer-Forschung",
        "imageUrl": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb",
        "source": "MIT Technology Review",
        "timestamp": (datetime.now() - timedelta(hours=1)).strftime("%d.%m.%Y %H:%M"),
        "summary": "Wissenschaftler haben einen bedeutenden Fortschritt in der Quantencomputer-Entwicklung erzielt. Das neue System kann bei Raumtemperatur arbeiten und verspricht praktische Anwendungen in naher Zukunft.",
        "relatedSources": [
            {"source": "MIT Technology Review", "url": "https://technologyreview.com/news/1"},
            {"source": "Nature", "url": "https://nature.com/articles/1"}
        ]
    },
    {
        "id": "news-4",
        "headline": "Neue Studie zeigt Zusammenhang zwischen Schlafqualität und mentaler Gesundheit",
        "imageUrl": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55",
        "source": "Science Daily",
        "timestamp": (datetime.now() - timedelta(minutes=45)).strftime("%d.%m.%Y %H:%M"),
        "summary": "Eine umfangreiche Studie mit über 10.000 Teilnehmern zeigt, dass schlechte Schlafqualität direkt mit einem erhöhten Risiko für psychische Erkrankungen verbunden ist. Die Forscher empfehlen neue Präventionsstrategien.",
        "relatedSources": [
            {"source": "Science Daily", "url": "https://sciencedaily.com/news/1"},
            {"source": "WHO", "url": "https://who.int/news/1"}
        ]
    },
    {
        "id": "news-5",
        "headline": "Künstliche Intelligenz revolutioniert Wettervorhersage",
        "imageUrl": "https://images.unsplash.com/photo-1592210454359-9043f067919b",
        "source": "Nature",
        "timestamp": (datetime.now() - timedelta(minutes=30)).strftime("%d.%m.%Y %H:%M"),
        "summary": "Ein neues KI-Modell kann Wettervorhersagen mit bisher unerreichter Genauigkeit erstellen. Das System analysiert historische Daten und aktuelle Satellitenmessungen in Echtzeit.",
        "relatedSources": [
            {"source": "Nature", "url": "https://nature.com/articles/2"},
            {"source": "Science", "url": "https://science.org/news/1"}
        ]
    },
    {
        "id": "news-6",
        "headline": "Neuer Rekord bei erneuerbaren Energien in Deutschland",
        "imageUrl": "https://images.unsplash.com/photo-1509391366360-2e959784a276",
        "source": "Der Spiegel",
        "timestamp": (datetime.now() - timedelta(minutes=15)).strftime("%d.%m.%Y %H:%M"),
        "summary": "Deutschland erreicht neuen Meilenstein: Über 50% des Strombedarfs wurden im letzten Monat durch erneuerbare Energien gedeckt. Experten sehen darin einen wichtigen Schritt zur Energiewende.",
        "relatedSources": [
            {"source": "Der Spiegel", "url": "https://spiegel.de/news/1"},
            {"source": "Tagesschau", "url": "https://tagesschau.de/news/1"}
        ]
    },
    {
        "id": "news-7",
        "headline": "Revolutionäre Behandlungsmethode für Alzheimer entdeckt",
        "imageUrl": "https://images.unsplash.com/photo-1576671081837-49000212a370",
        "source": "Medical News Today",
        "timestamp": (datetime.now() - timedelta(minutes=5)).strftime("%d.%m.%Y %H:%M"),
        "summary": "Forscher haben eine vielversprechende neue Behandlungsmethode für Alzheimer entwickelt. Die Therapie zielt auf die Grundursachen der Krankheit ab und zeigt in ersten klinischen Studien positive Ergebnisse.",
        "relatedSources": [
            {"source": "Medical News Today", "url": "https://medicalnewstoday.com/news/1"},
            {"source": "The Lancet", "url": "https://thelancet.com/articles/1"}
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
def read_root():
    return {"message": "Welcome to Papergum API"}

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
