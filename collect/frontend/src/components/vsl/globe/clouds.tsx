import { useRef } from 'react';
import * as THREE from "three"
import { useTexture } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'

type CloudsProps = {
  radius: number;
};

export default function Clouds({ radius }: CloudsProps) {
  const ref = useRef<THREE.Mesh>(null);
  const cloudsMap = useTexture("./textures/Clouds.png");

  useFrame(() => {
    if (ref.current) {
      ref.current.rotation.y += 0.00015;
    }
  });

  return (
    <mesh ref={ref}>
      <sphereGeometry args={[radius + 0.05, 64, 64]} />
      <meshStandardMaterial
        alphaMap={cloudsMap}
        transparent={true}
        opacity={0.3}
      />
    </mesh>
  );
}