'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import NewsCard from '@/components/NewsCard';

interface NewsItem {
  id: string;
  headline: string;
  imageUrl: string;
  source: string;
  timestamp: string;
  summary: string;
}

export default function Home() {
  const [newsItems, setNewsItems] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        console.log('Fetching news...');
        const response = await axios.get('http://localhost:8000/api/news');
        console.log('News data received:', response.data);
        setNewsItems(response.data);
      } catch (error) {
        console.error('Error fetching news:', error);
        setError('Fehler beim Laden der Nachrichten');
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Lade Nachrichten...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-600">
          <p>{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Erneut versuchen
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Aktuelle Nachrichten</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {newsItems.map((item) => (
            <NewsCard
              key={item.id}
              id={item.id}
              headline={item.headline}
              imageUrl={item.imageUrl}
              source={item.source}
              timestamp={item.timestamp}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
