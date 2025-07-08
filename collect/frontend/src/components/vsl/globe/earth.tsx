import { useRef } from "react";
import { useLoader, useFrame } from "@react-three/fiber";
import { Mesh } from "three";
import { TextureLoader } from "three";
import { Markers } from "@/components/vsl/globe/markers";

export function Earth({radius, markers}: {radius: number,markers: { lat: number, lon: number, ipfs_ea: string, ipfs_heatmap: string, ipfs_audio: string }[]}) {

  const ref = useRef<Mesh>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const texture = useLoader(TextureLoader, "/textures/albedo.jpg"); // Ton image
  const bumpMap = useLoader(TextureLoader, "/textures/normal.jpg"); // Ton image
  
  useFrame(() => {
    if (ref.current) {
      ref.current.rotation.y += 0.0001;
    }
  });
  
  return (
    <group ref={ref} position={[0, 0, 0]} rotation={[0, 0, 0]}>
      <mesh>
        <sphereGeometry args={[radius, 64, 64]} />
        <meshStandardMaterial 
          map={texture} 
          bumpMap={bumpMap}
          bumpScale={4}
          metalness={.5}
          roughness={0.7 }
          emissive={"#000022"}
          emissiveIntensity={0.5}
        />
      </mesh>

      <Markers
        radius={radius}
        markers={markers}
        onMarkerClick={(marker) => {
          console.log("🗺️ Tu as cliqué sur :", marker);

          const audioUrl = `https://ipfs.io/ipfs/${marker.ipfs_audio}`;

          // Arrête l'ancien son si encore en cours
          if (audioRef.current) {
            audioRef.current.pause();
            audioRef.current.currentTime = 0;
          }

          // Crée un nouveau son
          audioRef.current = new Audio(audioUrl);
          audioRef.current.play().catch((err) => {
            console.error("Erreur lecture audio :", err);
          });
        }}
      />

    </group>
  );
}