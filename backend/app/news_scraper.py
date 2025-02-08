import feedparser
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from typing import List, Dict
from datetime import datetime

class GermanNewsScraper:
    def __init__(self):
        self.sources = {
            'tagesschau': 'https://www.tagesschau.de/xml/rss2/',
            'ntv': 'https://www.n-tv.de/rss',
            'spiegel': 'https://www.spiegel.de/schlagzeilen/tops/index.rss'
        }

    def fetch_news(self) -> List[Dict]:
        all_news = []
        
        for source, url in self.sources.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:  # Get top 5 news from each source
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'source': source,
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                    }
                    
                    # Get full article text using newspaper3k
                    try:
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        news_item['full_text'] = article.text
                    except:
                        news_item['full_text'] = news_item['summary']
                    
                    all_news.append(news_item)
            except Exception as e:
                print(f"Error fetching news from {source}: {str(e)}")
                continue
        
        return all_news

    def get_main_points(self, news_items: List[Dict]) -> Dict:
        """
        Organize news by source and extract main points
        """
        organized_news = {
            'tagesschau': [],
            'ntv': [],
            'spiegel': []
        }
        
        for item in news_items:
            source = item['source']
            if source in organized_news:
                organized_news[source].append({
                    'title': item['title'],
                    'summary': item['summary'],
                    'link': item['link'],
                    'published': item['published']
                })
        
        return organized_news
