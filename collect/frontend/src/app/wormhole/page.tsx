"use client";

import { useState, useEffect } from "react";
import BkgShader from "@/components/vsl/wormhole/BkgShader";

export default function Wormhole({ onDone }: { onDone: () => void }) {
  const [lat, setLat] = useState(48.8566);
  const [lon, setLon] = useState(2.3522);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  useEffect(() => {
    if (!loading && response) {
      // Appelle le parent quand le travail est terminé
      onDone();
      setResponse(null);
    }
  }, [loading, response, onDone]);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLat(position.coords.latitude);
          setLon(position.coords.longitude);
        },
        (error) => {
          console.error("Erreur lors de la récupération de la position :", error);
        }
      );
    } else {
      console.warn("La géolocalisation n'est pas supportée par ce navigateur.");
    }
  }, []);

  const handleSharing = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_FASTAPI_URL}/api/core/wormhole/send_data`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          latitude: lat,
          longitude: lon,
          data: message,
        }),
      });

      if (!res.ok) {
        throw new Error(`Erreur serveur: ${res.status}`);
      }

      const data = await res.json();
      console.log("Réponse de l'API :", data);
      setResponse(data.result);
    } catch (error) {
      console.error("Erreur lors de l'envoi :", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center">
      <BkgShader />

      <div className="w-128 p-6 bg-black/40 backdrop-blur-md rounded-2xl shadow-md border border-gray-500 relative z-10">
        <h2 className="text-2xl font-bold mb-6 text-center text-white">Wormhole</h2>
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-gray-200 font-semibold mb-2">Latitude</label>
            <input
              type="number"
              value={lat}
              onChange={(e) => setLat(parseFloat(e.target.value))}
              className="w-full border border-gray-600 bg-black/30 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-gray-200 font-semibold mb-2">Longitude</label>
            <input
              type="number"
              value={lon}
              onChange={(e) => setLon(parseFloat(e.target.value))}
              className="w-full border border-gray-600 bg-black/30 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-gray-200 font-semibold mb-2">Texte</label>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full border border-gray-600 bg-black/30 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          onClick={handleSharing}
          className="w-1/4 mx-auto block bg-blue-800 text-white py-3 rounded-lg border border-gray-500 font-semibold hover:bg-blue-700 transition-colors"
        >
          {loading ? <span className="ml-2">Sending...</span> : "Send"}
        </button>

        {response && (
          <div className="block mt-4 text-center text-white">
            <pre className="text-[10px] bg-black/30 p-4 rounded-lg overflow-x-auto break-words whitespace-pre-wrap max-h-40 overflow-y-auto">
              {response}
            </pre>
         </div>
        )}
      </div>
    </div>
  );
}
