// clock.tsx

'use client';

import { useEffect, useState } from 'react';

export default function Clock() {
  const [time, setTime] = useState('');

  useEffect(() => {
    const updateTime = () => {
      setTime(new Date().toLocaleTimeString());
    };

    updateTime(); // Init tout de suite

    const interval = setInterval(updateTime, 1000); // Update chaque seconde

    return () => clearInterval(interval); // Nettoyage
  }, []);

  return <p>Heure actuelle: {time || '...'}</p>;
}
