import { useState, useEffect, useRef } from "react";
import { Vector3, Quaternion, ShaderMaterial } from "three";
import { geo } from "@/components/utils/geo";
import { vertexShader, fragmentShader } from "@/components/vsl/globe/shaders/markerShader";
import { useFrame} from "@react-three/fiber";
import { TextureLoader } from "three";
import * as THREE from 'three';

export function Markers({
  radius,
  markers,
  onMarkerClick,
}: {
  radius: number;
  markers: { lat: number; lon: number; ipfs_ea: string; ipfs_heatmap: string; ipfs_audio: string }[];
  onMarkerClick?: (marker: { lat: number; lon: number; ipfs_audio: string }) => void;
}) {
  const GATEWAY_URL = "https://ipfs.io/ipfs/";
  const rows = 100;
  const cycleDuration = 1.0;

  // ✅ État local pour stocker les textures par marker
  const [textures, setTextures] = useState<{ [key: string]: THREE.Texture }>({});
  const materialsRef = useRef<{ [key: string]: ShaderMaterial }>({});

  // Charger *seulement* les nouvelles textures
  useEffect(() => {
    const loader = new TextureLoader();
    markers.forEach(m => {
      if (!m.ipfs_heatmap) return;
      const key = m.ipfs_heatmap;
      if (!textures[key]) {
        loader.load(
          `${GATEWAY_URL}${key}`,
          texture => {
            setTextures(prev => ({ ...prev, [key]: texture }));
          },
          undefined,
          err => {
            console.warn(`Failed to load texture for ${key}`, err);
          }
        );
      }
    });
  }, [markers, textures]);

  useFrame(({ clock }) => {
    Object.values(materialsRef.current).forEach(mat => {
      mat.uniforms.u_time.value = clock.elapsedTime;
    });
  });

  return (
    <>
      {markers.map((m, idx) => {
        const pos = geo(m.lat, m.lon, radius);
        const normal = pos.clone().normalize();
        const offset = normal.clone().multiplyScalar(0.01);
        const finalPos = pos.clone().add(offset);

        const up = new Vector3(0, 0, 1);
        const quaternion = new Quaternion().setFromUnitVectors(up, normal);

        const tex = textures[m.ipfs_heatmap];
        if (!tex) return null;

        // 🔑 Créer et stocker le ShaderMaterial UNE FOIS
        if (!materialsRef.current[m.ipfs_heatmap]) {
          materialsRef.current[m.ipfs_heatmap] = new ShaderMaterial({
            vertexShader,
            fragmentShader,
            uniforms: {
              u_time: { value: 0 },
              u_colors: { value: tex },
              u_rows: { value: rows },
              u_cycleDuration: { value: cycleDuration }
            },
            transparent: false,
          });
        }

        const material = materialsRef.current[m.ipfs_heatmap];

        return (
          <mesh
            key={idx}
            position={finalPos.toArray()}
            quaternion={quaternion}
            onClick={() => onMarkerClick?.(m)}
          >
            <circleGeometry args={[0.02, 32]} />
            <primitive object={material} attach="material" />
          </mesh>
        );
      })}
    </>
  );
}
