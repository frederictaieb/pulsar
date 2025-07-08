"use client";

import { useState, useCallback } from "react";
import XrpListener from "@/components/web3/xrp/XrpListener";
import { Scene } from "@/components/vsl/globe/scene";
import Wormhole from "@/app/wormhole/page"; // Ajuste l'import si nécessaire

export default function Home() {
  const [markers, setMarkers] = useState<{
    lat: number,
    lon: number,
    ipfs_ea: string,
    ipfs_heatmap: string,
    ipfs_audio: string
  }[]>([]);

  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const addMarker = useCallback((
    lat: number,
    lon: number,
    ipfs_ea: string,
    ipfs_heatmap: string,
    ipfs_audio: string
  ) => {
    setMarkers(prev => [...prev, { lat, lon, ipfs_ea, ipfs_heatmap, ipfs_audio }]);
  }, []);

  return (
    <div className="relative min-h-screen overflow-hidden">
      <Scene markers={markers} />
      <XrpListener addMarker={addMarker} />

      {/* Bouton SVG centré en haut */}
      <button
        onClick={() => setIsDrawerOpen(!isDrawerOpen)}
        className={`
          fixed top-4 left-4 
          p-2 rounded-full z-50 transition-colors
          ${isDrawerOpen ? 'bg-white/20' : 'bg-white/10 hover:bg-white/20'}
        `}
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 424" className="w-8 h-8 fill-white">
          <path d="M437,0h74L357,152.48c-55.77,55.19-146.19,55.19-202,0L.94,0H75L192,115.83a91.11,91.11,0,0,0,127.91,0Z"/>
          <path d="M74.05,424H0L155,270.58c55.77-55.19,146.19-55.19,202,0L512,424H438L320,307.23a91.11,91.11,0,0,0-127.91,0Z"/>
        </svg>
      </button>

      {/* Tiroir */}
      <div className={`fixed inset-x-0 bottom-0 bg-black/50 backdrop-blur-md transition-transform duration-500 ${isDrawerOpen ? "translate-y-0" : "translate-y-full"} rounded-t-3xl shadow-lg z-40`}>
        <div className="relative p-4 pt-10 z-10">
          <Wormhole onDone={() => setIsDrawerOpen(false)} />
        </div>
      </div>
    </div>
  );
}
