"use client";

import { useState, useEffect } from "react";
import useXrpListener from "@/hooks/web3/xrp/useXrpListener";

type XrpMessage = {
  timestamp: string;
  latitude: string;
  longitude: string;
  ipfs_ea: string;
  ipfs_heatmap: string;
  ipfs_audio: string;
};

export default function XrpListener({
  addMarker,
}: {
  addMarker: (
    lat: number,
    lon: number,
    ipfs_ea: string,
    ipfs_heatmap: string,
    ipfs_audio: string
  ) => void;
}) {
  const walletAddress = process.env.NEXT_PUBLIC_DST_ADDR;
  const messageContent = useXrpListener(walletAddress);

  const [jsonData, setJsonData] = useState<XrpMessage | null>(null);
  const [timestamp, setTimestamp] = useState("");
  const [latitude, setLatitude] = useState(0.0);
  const [longitude, setLongitude] = useState(0.0);

  useEffect(() => {
    if (!messageContent) return;

    try {
      const parsedMesssageContent = JSON.parse(messageContent);
      setJsonData(parsedMesssageContent);
    } catch (err) {
      console.error("Invalid JSON:", err);
    }
  }, [messageContent]);

  useEffect(() => {
    if (!jsonData) return;

    const dateObj = new Date(jsonData.timestamp);
    const yyyy = dateObj.getFullYear();
    const mm = String(dateObj.getMonth() + 1).padStart(2, "0");
    const dd = String(dateObj.getDate()).padStart(2, "0");
    const hh = String(dateObj.getHours()).padStart(2, "0");
    const min = String(dateObj.getMinutes()).padStart(2, "0");
    const timestamp_fmt = `${yyyy}-${mm}-${dd} ${hh}:${min}`;

    const latitude_fmt = parseFloat(jsonData.latitude);
    const longitude_fmt = parseFloat(jsonData.longitude);

    const ipfs_ea = jsonData.ipfs_ea;
    const ipfs_heatmap = jsonData.ipfs_heatmap;
    const ipfs_audio = jsonData.ipfs_audio;

    setTimestamp(timestamp_fmt);
    setLatitude(latitude_fmt);
    setLongitude(longitude_fmt);

    addMarker(latitude_fmt, longitude_fmt, ipfs_ea, ipfs_heatmap, ipfs_audio);
  }, [jsonData, addMarker]);

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 w-full flex justify-center pointer-events-none px-4">
      <div className="w-1/2 p-4 bg-black/50 text-white/70 text-sm rounded-xl shadow-md min-h-[40px] flex flex-col space-y-1 border border-gray-900">
        {timestamp
          ? `Last message received from ${latitude.toFixed(
              4
            )}, ${longitude.toFixed(4)} at ${timestamp}`
          : ""}
      </div>
    </div>
  );
}
