"use client";
import { useMemo, useRef } from "react";
import { Vector3, Mesh, Quaternion } from "three";
import { useFrame } from "@react-three/fiber";
import { geo } from "@/components/utils/geo";

export function Markers({ radius, markers }: { radius: number; markers: { lat: number; lon: number }[] }) {
  const baseHeight = 0.2; // longueur du bâton

  const positions = useMemo(() => {
    return markers.map(({ lat, lon }) => geo(lat, lon, radius));
  }, [markers, radius]);

  const refs = useRef<(Mesh | null)[]>([]);

  useFrame(() => {
    refs.current.forEach((mesh) => {
      if (mesh) {
        // Animation d'apparition
        const s = mesh.scale.y;
        if (s < 1) {
          const newScale = s + 0.05;
          mesh.scale.y = Math.min(newScale, 1);
        }
      }
    });
  });

  return (
    <>
      {positions.map((pos, idx) => {
        // La normale : vecteur du centre vers la surface
        const normal = pos.clone().normalize();
        // Position décalée : on décale le cylindre le long de la normale
        const offset = normal.clone().multiplyScalar(baseHeight / 2);
        const finalPos = pos.clone().add(offset);

        // Calcul de la rotation pour aligner l'axe Y du cylindre avec la normale
        const up = new Vector3(0, 1, 0); // axe Y
        const quaternion = new Quaternion().setFromUnitVectors(up, normal);

        return (
          <mesh
            key={idx}
            position={finalPos.toArray()}
            quaternion={quaternion}
            ref={(el) => (refs.current[idx] = el)}
            scale={[1, 0, 1]} // Start scaleY = 0 pour animation
          >
            <cylinderGeometry args={[0.01, 0.01, baseHeight, 32]} />
            <meshStandardMaterial color="red" emissive="red" emissiveIntensity={1} />
          </mesh>
        );
      })}
    </>
  );
}
