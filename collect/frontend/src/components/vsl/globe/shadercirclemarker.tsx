"use client";

import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { ShaderMaterial, Vector3, Quaternion } from "three";

export function ShaderCircleMarker({
  position,
  normal,
  radius = 0.1,
  onClick,
}: {
  position: Vector3;
  normal: Vector3;
  radius?: number;
  onClick?: () => void;
}) {
  const materialRef = useRef<ShaderMaterial>(null!);

  useFrame(({ clock, size }) => {
    if (materialRef.current) {
      materialRef.current.uniforms.iTime.value = clock.getElapsedTime();
      materialRef.current.uniforms.iResolution.value.set(size.width, size.height, 1);
    }
  });

  const up = new Vector3(0, 0, 1);
  const quat = new Quaternion().setFromUnitVectors(up, normal.clone().normalize());

  // Décalé pour être bien hors du globe mais sous les nuages
  const offsetPos = position.clone().add(normal.clone().multiplyScalar(0.045));

  return (
    <mesh
      position={offsetPos}
      quaternion={quat}
      onClick={(e) => {
        e.stopPropagation();
        if (onClick) onClick();
      }}
    >
      <circleGeometry args={[radius, 64]} />
      <shaderMaterial
        ref={materialRef}
        side={2}
        transparent
        depthTest={true} // ✅ On garde le Z-buffer
        depthWrite={true}
        uniforms={{
          iTime: { value: 0 },
          iResolution: { value: new Vector3() },
        }}
        vertexShader={`
          varying vec2 vUv;
          void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `}
        fragmentShader={`
          varying vec2 vUv;
          uniform float iTime;
          uniform vec3 iResolution;

          vec3 palette(float d){
            return mix(vec3(0.2,0.7,0.9),vec3(1.,0.,1.),d);
          }

          vec2 rotate(vec2 p,float a){
            float c = cos(a);
            float s = sin(a);
            return p*mat2(c,s,-s,c);
          }

          float map(vec3 p){
            for( int i = 0; i<8; ++i){
              float t = iTime*0.2;
              p.xz = rotate(p.xz,t);
              p.xy = rotate(p.xy,t*1.89);
              p.xz = abs(p.xz);
              p.xz -= .5;
            }
            return dot(sign(p),p)/5.;
          }

          vec3 rm (vec3 ro, vec3 rd){
            float t = 0.;
            vec3 col = vec3(0.);
            float d;
            for(float i = 0.; i<64.; i++){
              vec3 p = ro + rd*t;
              d = map(p)*.5;
              if(d<0.02) break;
              if(d>100.) break;
              col += palette(length(p)*.1)/(400.*(d));
              t += d;
            }
            return col;
          }

          void main() {
            vec2 fragCoord = vUv * iResolution.xy;
            vec2 uv = (fragCoord - (iResolution.xy/2.)) / iResolution.x;
            vec3 ro = vec3(0.,0.,-50.);
            ro.xz = rotate(ro.xz,iTime);
            vec3 cf = normalize(-ro);
            vec3 cs = normalize(cross(cf,vec3(0.,1.,0.)));
            vec3 cu = normalize(cross(cf,cs));
            vec3 uuv = ro+cf*3. + uv.x*cs + uv.y*cu;
            vec3 rd = normalize(uuv-ro);
            vec3 col = rm(ro,rd);
            gl_FragColor = vec4(col, 1.0);
          }
        `}
      />
    </mesh>
  );
}
