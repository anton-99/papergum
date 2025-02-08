'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import axios from 'axios';
import Image from 'next/image';
import Link from 'next/link';

interface NewsDetail {
  id: string;
  headline: string;
  imageUrl: string;
  source: string;
  timestamp: string;
  summary: string;
  relatedSources: {
    source: string;
    url: string;
  }[];
}

export default function NewsDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [newsDetail, setNewsDetail] = useState<NewsDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNewsDetail = async () => {
      try {
        console.log('Fetching news detail for ID:', id);
        const response = await axios.get(`http://localhost:8000/api/news/${id}`);
        console.log('News detail data:', response.data);
        setNewsDetail(response.data);
      } catch (error: any) {
        console.error('Error fetching news detail:', error);
        setError(error.response?.data?.detail || 'Fehler beim Laden des Artikels');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchNewsDetail();
    }
  }, [id]);

  if (!id) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-600">
          <p>Ungültige Artikel-ID</p>
          <Link href="/" className="mt-4 inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Zurück zur Übersicht
          </Link>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Lade Artikel...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <Link href="/" className="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Zurück zur Übersicht
          </Link>
        </div>
      </div>
    );
  }

  if (!newsDetail) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl mb-4">Artikel nicht gefunden</p>
          <Link href="/" className="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Zurück zur Übersicht
          </Link>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <Link href="/" className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Zurück zur Übersicht
        </Link>

        <article className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="relative h-96 w-full">
            <Image
              src={newsDetail.imageUrl}
              alt={newsDetail.headline}
              fill
              style={{ objectFit: 'cover' }}
              priority
            />
          </div>

          <div className="p-6">
            <div className="flex justify-between items-center text-sm text-gray-600 mb-4">
              <span>{newsDetail.source}</span>
              <span>{newsDetail.timestamp}</span>
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-6">{newsDetail.headline}</h1>
            
            <div className="prose max-w-none">
              <p className="text-gray-700 text-lg leading-relaxed mb-8">{newsDetail.summary}</p>
            </div>

            {newsDetail.relatedSources && newsDetail.relatedSources.length > 0 && (
              <div className="border-t pt-6 mt-8">
                <h2 className="text-xl font-semibold mb-4">Weitere Quellen</h2>
                <ul className="space-y-3">
                  {newsDetail.relatedSources.map((source, index) => (
                    <li key={index}>
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800"
                      >
                        {source.source}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </article>
      </div>
    </main>
  );
}
