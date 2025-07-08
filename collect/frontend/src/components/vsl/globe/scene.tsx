"use client";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera } from "@react-three/drei";
import { Earth } from "@/components/vsl/globe/earth";
import Atmosphere from './atmosphere';
import Clouds from './clouds';
import Lights from './lights';
import IcecastPlayer from "@/components/snd/IcecastPlayer";

//export function Scene() {
export function Scene({markers}: {markers: { lat: number, lon: number, ipfs_ea: string, ipfs_heatmap: string, ipfs_audio: string }[]}) {


  const radius = 2;
  const withAtmosphere = true;
  const withClouds = true;

  return (
    <div className="flex justify-center items-center h-screen bg-black">
      <div className="absolute top-0 left-0 w-full h-full">
        <IcecastPlayer />
      </div>
      <Canvas className="h-2xl w-2xl">
        <PerspectiveCamera makeDefault fov={32} position={[0, 0, 8]} />
        <Lights/>
        <Earth radius={2} markers={markers}/>
        {withAtmosphere && <Atmosphere radius={radius}/>}
        {withClouds && <Clouds radius={radius}/>}
        <OrbitControls target={[0, -0.1, 0]}/>
      </Canvas>
    </div>
  );
}

