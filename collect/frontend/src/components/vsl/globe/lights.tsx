export default function Lights() {
  return (
    <>
      <pointLight position={[0, 0, 5]} intensity={10} distance={0} decay={0.5} />

      <directionalLight
        intensity={5}
        position={[5, 5, 5]}
        castShadow
      />
      <directionalLight
        intensity={3}
        position={[-5, -5, 3]}
        castShadow
      />
      <ambientLight intensity={1} />
    </>
  )
}