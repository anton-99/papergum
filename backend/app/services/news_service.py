import feedparser
from newspaper import Article
from typing import List, Dict, Optional
import uuid
from datetime import datetime, timedelta
import logging
import asyncio
from functools import lru_cache
import aiohttp
from bs4 import BeautifulSoup
from ..models.news import NewsDetail, RelatedSource

logger = logging.getLogger(__name__)

# Cache for storing parsed news items
NEWS_CACHE = {}
CACHE_DURATION = timedelta(minutes=5)

NEWS_SOURCES = [
    {
        "name": "Tagesschau",
        "url": "https://www.tagesschau.de/xml/rss2/",
        "language": "de"
    },
    {
        "name": "Zeit Online",
        "url": "https://newsfeed.zeit.de/index",
        "language": "de"
    },
    {
        "name": "Spiegel Online",
        "url": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
        "language": "de"
    }
]

async def fetch_article_content(session: aiohttp.ClientSession, url: str) -> Dict:
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return {
                    "image_url": "https://images.unsplash.com/photo-1504711434969-e33886168f5c",
                    "text": ""
                }
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try to find the main article image
            image_url = "https://images.unsplash.com/photo-1504711434969-e33886168f5c"
            img_tags = soup.find_all('img')
            for img in img_tags:
                src = img.get('src', '')
                if src and (src.startswith('http') or src.startswith('//')):
                    image_url = src if src.startswith('http') else f"https:{src}"
                    break
            
            # Try to find the main article text
            article_text = ""
            article_tags = soup.find_all(['p', 'article'])
            for tag in article_tags:
                text = tag.get_text().strip()
                if len(text) > 100:  # Only include substantial paragraphs
                    article_text += text + "\n\n"
            
            return {
                "image_url": image_url,
                "text": article_text[:500] + "..." if len(article_text) > 500 else article_text
            }
    except Exception as e:
        logger.error(f"Error fetching article {url}: {str(e)}")
        return {
            "image_url": "https://images.unsplash.com/photo-1504711434969-e33886168f5c",
            "text": ""
        }

async def get_latest_news_async() -> List[NewsDetail]:
    # Check cache first
    cache_key = "latest_news"
    if cache_key in NEWS_CACHE:
        cache_time, cached_news = NEWS_CACHE[cache_key]
        if datetime.now() - cache_time < CACHE_DURATION:
            return cached_news

    news_items = []
    async with aiohttp.ClientSession() as session:
        for source in NEWS_SOURCES:
            try:
                feed = feedparser.parse(source["url"])
                tasks = []
                
                for entry in feed.entries[:3]:  # Get top 3 news from each source
                    tasks.append(fetch_article_content(session, entry.link))
                
                # Fetch all articles concurrently
                article_data_list = await asyncio.gather(*tasks, return_exceptions=True)
                
                for entry, article_data in zip(feed.entries[:3], article_data_list):
                    try:
                        if isinstance(article_data, Exception):
                            logger.error(f"Error processing entry from {source['name']}: {str(article_data)}")
                            continue
                            
                        # Generate a deterministic ID based on the news URL
                        news_id = str(uuid.uuid5(uuid.NAMESPACE_URL, entry.link))
                        
                        news_item = NewsDetail(
                            id=news_id,
                            headline=entry.title,
                            imageUrl=article_data["image_url"],
                            source=source["name"],
                            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M"),
                            summary=article_data["text"] if article_data["text"] else entry.get("summary", ""),
                            relatedSources=[
                                RelatedSource(source=source["name"], url=entry.link)
                            ]
                        )
                        news_items.append(news_item)
                    except Exception as e:
                        logger.error(f"Error processing entry from {source['name']}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"Error fetching news from {source['name']}: {str(e)}")
                continue
    
    # Sort by timestamp (newest first) and limit to 10 items
    result = sorted(news_items, key=lambda x: x.timestamp, reverse=True)[:10]
    
    # Update cache
    NEWS_CACHE[cache_key] = (datetime.now(), result)
    
    return result

def get_latest_news() -> List[NewsDetail]:
    """Synchronous wrapper for the async function"""
    return asyncio.run(get_latest_news_async())
