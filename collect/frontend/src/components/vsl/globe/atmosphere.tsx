import { useRef } from 'react';
import * as THREE from "three"
import { useFrame } from '@react-three/fiber'

type AtmosphereProps = {
  radius: number;
};

export default function Atmosphere({ radius }: AtmosphereProps) {
  const ref = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (ref.current) {
      ref.current.rotation.y += 0.0002;
    }
  });

  return (
    <mesh ref={ref}>
      <sphereGeometry args={[1.195 * radius, 64, 64]} />
      <shaderMaterial
               vertexShader={
                `
                varying vec3 vNormal;
                varying vec3 eyeVector;

                void main() {
                  vec4 mvPos = modelViewMatrix * vec4( position, 1.0 );
                  vNormal = normalize( normalMatrix * normal );
                  eyeVector = normalize(mvPos.xyz);
                  gl_Position = projectionMatrix * mvPos;
                }
                `
              }
              fragmentShader={
                `
                varying vec3 vNormal;
                varying vec3 eyeVector;
                uniform float atmOpacity;
                uniform float atmPowFactor;
                uniform float atmMultiplier;

                void main() {
                  float dotP = dot( vNormal, eyeVector );
                  float factor = pow(dotP, atmPowFactor) * atmMultiplier;
                  vec3 atmColor = vec3(0.35 + dotP/4.5, 0.35 + dotP/4.5, 1.0);
                  gl_FragColor = vec4(atmColor, atmOpacity) * factor;
                }`
              }
              uniforms={{
                atmOpacity: { value: 0.7 },
                atmPowFactor: { value: 4.1 },
                atmMultiplier: { value: 9.5 },
              }}
              blending={THREE.AdditiveBlending}
              side={THREE.BackSide}
      />
    </mesh>
  );
}
