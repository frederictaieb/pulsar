"use client";

import { useState, useRef } from 'react';

export default function IcecastPlayer() {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  const togglePlay = () => {
    if (!audioRef.current) return;

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="flex p-2 justify-end bg-transparent">
      <audio
        ref={audioRef}
        onPause={() => setIsPlaying(false)}
        onPlay={() => setIsPlaying(true)}
      >
        <source
          src={process.env.NEXT_PUBLIC_ICECAST_URL}
          type="audio/mpeg"
        />
      </audio>

      <button
        onClick={togglePlay}
        className={`
          fixed top-4 right-4
          p-2 rounded-full z-50 transition-colors
          ${isPlaying ? 'bg-white/20' : 'bg-white/10 hover:bg-white/20'}
        `}
      >
        {isPlaying ? (
          // Speaker ON
          <svg viewBox="0 0 100 100" className="w-8 h-8 fill-white">
            <polygon
              points="38,15 40,15 40,85 38,85 15,60 4,60 4,40 15,40"
              style={{ fill: "white", fillOpacity: 0.9, stroke: "white", strokeWidth: 2 }}
            />
            <path d="m 51,24 c 16,15 16,38 1,53" style={{ fill: "none", stroke: "white", strokeWidth: 7 }} />
            <path d="m 62,14 c 37,38 1,73 1,73" style={{ fill: "none", stroke: "white", strokeWidth: 7 }} />
            <path d="M 72,5 C 120,54 73,97 73,97" style={{ fill: "none", stroke: "white", strokeWidth: 7 }} />
          </svg>
        ) : (
          // Speaker OFF
          <svg viewBox="0 0 100 100" className="w-8 h-8 fill-gray-400">
            <polygon
              points="38,15 40,15 40,85 38,85 15,60 4,60 4,40 15,40"
              style={{ fill: "gray", fillOpacity: 0.7, stroke: "gray", strokeWidth: 2 }}
            />
            <path d="m 51,24 c 16,15 16,38 1,53" style={{ fill: "none", stroke: "gray", strokeWidth: 7 }} />
            <path d="m 62,14 c 37,38 1,73 1,73" style={{ fill: "none", stroke: "gray", strokeWidth: 7 }} />
            <path d="M 72,5 C 120,54 73,97 73,97" style={{ fill: "none", stroke: "gray", strokeWidth: 7 }} />
            <line x1="10" y1="10" x2="90" y2="90" stroke="gray" strokeWidth="6" />
          </svg>
        )}
      </button>
    </div>
  );
}
