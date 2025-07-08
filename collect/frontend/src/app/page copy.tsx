"use client";
import { useState } from "react";
import IcecastPlayer from "@/components/snd/IcecastPlayer";
import XrpListener from "@/components/web3/xrp/XrpListener";
import { Scene } from "@/components/vsl/globe/scene";


export default function Home() {

  const [markers, setMarkers] = useState<{ lat: number, lon: number, ipfs_ea: string, ipfs_heatmap: string, ipfs_audio: string }[]>([]);

  return (
    <div>
        <IcecastPlayer />
        <Scene markers={markers} />
        <XrpListener 
            addMarker={(lat: number, lon: number, ipfs_ea: string, ipfs_heatmap: string, ipfs_audio: string) => {
            setMarkers(prev => [...prev, { lat, lon, ipfs_ea, ipfs_heatmap, ipfs_audio }]);
          }} 
        />
    </div>
  );
}