from fastapi import APIRouter, HTTPException
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.news_scraper import GermanNewsScraper

router = APIRouter()
news_scraper = GermanNewsScraper()

@router.get("/german-news", tags=["news"])
async def get_german_news():
    """
    Fetch news from German news sources (tagesschau, n-tv, and Der Spiegel)
    """
    try:
        news_items = news_scraper.fetch_news()
        organized_news = news_scraper.get_main_points(news_items)
        return organized_news
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
