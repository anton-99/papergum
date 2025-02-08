'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useState } from 'react';

interface NewsCardProps {
  id: string;
  headline: string;
  imageUrl: string;
  source: string;
  timestamp: string;
}

export default function NewsCard({ id, headline, imageUrl, source, timestamp }: NewsCardProps) {
  const [imageError, setImageError] = useState(false);

  const handleImageError = () => {
    console.log('Image failed to load:', imageUrl);
    setImageError(true);
  };

  return (
    <Link href={`/news/${id}`} className="block">
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
        <div className="relative h-48 w-full bg-gray-200">
          {!imageError ? (
            <Image
              src={imageUrl}
              alt={headline}
              fill
              style={{ objectFit: 'cover' }}
              className="transition-transform duration-300 hover:scale-105"
              onError={handleImageError}
              priority
            />
          ) : (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-200">
              <span className="text-gray-400">Bild nicht verfügbar</span>
            </div>
          )}
        </div>
        <div className="p-4">
          <h2 className="text-xl font-semibold line-clamp-2 mb-2">{headline}</h2>
          <div className="flex justify-between items-center text-sm text-gray-600">
            <span>{source}</span>
            <span>{timestamp}</span>
          </div>
        </div>
      </div>
    </Link>
  );
}
