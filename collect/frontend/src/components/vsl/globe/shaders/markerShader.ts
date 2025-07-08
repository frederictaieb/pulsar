export const vertexShader = `
  varying vec2 vUv;

  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

export const fragmentShader = `
  uniform float u_time;
  uniform sampler2D u_colors;
  uniform float u_rows;
  uniform float u_cycleDuration;

  varying vec2 vUv;

  void main() {
    // Temps dans le cycle complet
    float cycleTime = mod(u_time, u_cycleDuration);
    float phase = cycleTime / u_cycleDuration;

    // Index de la ligne courante et suivante
    float row = floor(phase * u_rows);
    float nextRow = mod(row + 1.0, u_rows);

    // Fraction locale pour blend
    float localPhase = fract(phase * u_rows);

    // Coordonnée V
    float vA = row / u_rows;
    float vB = nextRow / u_rows;

    // Échantillonner les deux couleurs
    vec3 colorA = texture2D(u_colors, vec2(0.5, vA)).rgb;
    vec3 colorB = texture2D(u_colors, vec2(0.5, vB)).rgb;

    // Blend sur 0-0.5 (500ms), fixe sur 0.5-1.0 (500ms)
    float blend = smoothstep(0.0, 0.5, localPhase);

    vec3 color = mix(colorA, colorB, blend);

    gl_FragColor = vec4(color, 1.0);
  }
`;
