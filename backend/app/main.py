from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime, timedelta
import logging
import sys
import os
import traceback

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import news
from app.services.news_service import get_latest_news
from app.models.news import NewsDetail

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Papergum API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the news router
app.include_router(news.router, tags=["news"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Papergum API"}

@app.get("/api/news", response_model=List[NewsDetail])
def get_news():
    try:
        logger.info("Fetching latest news")
        news_items = get_latest_news()
        logger.info(f"Successfully fetched {len(news_items)} news items")
        return news_items
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.get("/api/news/{news_id}", response_model=NewsDetail)
def get_news_detail(news_id: str):
    try:
        logger.info(f"Fetching news detail for ID: {news_id}")
        news_items = get_latest_news()
        for news in news_items:
            if news.id == news_id:
                logger.info(f"Found news item with ID: {news_id}")
                return news
        logger.warning(f"News item not found with ID: {news_id}")
        raise HTTPException(status_code=404, detail="News not found")
    except Exception as e:
        logger.error(f"Error fetching news detail: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error fetching news detail: {str(e)}")
