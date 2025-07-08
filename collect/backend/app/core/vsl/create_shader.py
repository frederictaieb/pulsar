ef screate_shader(rgb_colors, switch_interval=1.0, transition_ratio=0.5):
    """
    Génère un shader GLSL ShaderToy :
    chaque couleur reste fixe (1 - transition_ratio) du temps,
    puis transitionne vers la suivante sur transition_ratio du temps.

    Args:
        rgb_colors (list of tuple): Liste [(r, g, b)] entre 0..1.
        switch_interval (float): Durée totale par couleur (secondes).
        transition_ratio (float): Fraction de l'intervalle pour la transition [0, 1].

    Returns:
        str: Code GLSL prêt pour ShaderToy.
    """
    vec_colors = ",\n    ".join([
        f"vec3({r:.4f}, {g:.4f}, {b:.4f})"
        for (r, g, b) in rgb_colors
    ])
    num_colors = len(rgb_colors)

    shader_code = f"""
// ShaderToy shader : switch avec transition paramétrable

vec3 colors[{num_colors}] = vec3[](
    {vec_colors}
);

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;

    float t = mod(iTime, {switch_interval} * {num_colors}.0);
    float idx_f = floor(t / {switch_interval});
    float phase = mod(t, {switch_interval}) / {switch_interval};

    int i0 = int(idx_f);
    int i1 = (i0 + 1) % {num_colors};

    vec3 c0 = colors[i0];
    vec3 c1 = colors[i1];

    float transition = {transition_ratio};
    float blend = 0.0;

    if (phase > (1.0 - transition)) {{
        blend = (phase - (1.0 - transition)) / transition;
    }}

    vec3 color = mix(c0, c1, blend);

    fragColor = vec4(color, 1.0);
}}
"""
    return shader_code


def create_heatmap(emotions_batch, resolution=100):
    df = process_data_json(emotions_batch)
    df = analyze_emotions(df)
    list_colors = emotions_to_colors(df)
    heatmap_path = create_heatmap(list_colors, resolution)
    return heatmap_path
    
"""
if __name__ == "__main__":
    emotions_batch = [
        {'emotions': {'neutral': 0.2999, 'anger': 0.0446, 'disgust': 0.1591, 'joy': 0.0588, 'fear': 0.1139, 'sadness': 0.2753, 'surprise': 0.0483}, 'evi': 0.55},
        {'emotions': {'neutral': 0.0966, 'anger': 0.3017, 'disgust': 0.1138, 'joy': 0.2070, 'fear': 0.0789, 'sadness': 0.1015, 'surprise': 0.1005}, 'evi': 0.67},
        {'emotions': {'neutral': 0.1862, 'anger': 0.1372, 'disgust': 0.1200, 'joy': 0.1976, 'fear': 0.1444, 'sadness': 0.1248, 'surprise': 0.0898}, 'evi': 0.31},
        {'emotions': {'neutral': 0.1553, 'anger': 0.1151, 'disgust': 0.0291, 'joy': 0.3092, 'fear': 0.1743, 'sadness': 0.1008, 'surprise': 0.1162}, 'evi': 0.77},
        {'emotions': {'neutral': 0.0742, 'anger': 0.1174, 'disgust': 0.0492, 'joy': 0.0550, 'fear': 0.2254, 'sadness': 0.4203, 'surprise': 0.0585}, 'evi': 0.66},
        {'emotions': {'neutral': 0.0678, 'anger': 0.1821, 'disgust': 0.2581, 'joy': 0.1075, 'fear': 0.0353, 'sadness': 0.2103, 'surprise': 0.1389}, 'evi': 0.94},
        {'emotions': {'neutral': 0.1252, 'anger': 0.0976, 'disgust': 0.1937, 'joy': 0.1361, 'fear': 0.1714, 'sadness': 0.1455, 'surprise': 0.1305}, 'evi': 0.89},
        {'emotions': {'neutral': 0.1742, 'anger': 0.1814, 'disgust': 0.0759, 'joy': 0.0956, 'fear': 0.2215, 'sadness': 0.2046, 'surprise': 0.0467}, 'evi': 0.74},
        {'emotions': {'neutral': 0.1336, 'anger': 0.2345, 'disgust': 0.1388, 'joy': 0.1091, 'fear': 0.1717, 'sadness': 0.0984, 'surprise': 0.1139}, 'evi': 0.91},
        {'emotions': {'neutral': 0.2167, 'anger': 0.1065, 'disgust': 0.1098, 'joy': 0.1528, 'fear': 0.1307, 'sadness': 0.1135, 'surprise': 0.1700}, 'evi': 0.19},
        {'emotions': {'neutral': 0.2514, 'anger': 0.0762, 'disgust': 0.1011, 'joy': 0.1447, 'fear': 0.1811, 'sadness': 0.1065, 'surprise': 0.1389}, 'evi': 0.72},
        {'emotions': {'neutral': 0.1904, 'anger': 0.0685, 'disgust': 0.0972, 'joy': 0.1043, 'fear': 0.1969, 'sadness': 0.2106, 'surprise': 0.1321}, 'evi': 0.37},
        {'emotions': {'neutral': 0.1128, 'anger': 0.1243, 'disgust': 0.0867, 'joy': 0.1956, 'fear': 0.1768, 'sadness': 0.1313, 'surprise': 0.1725}, 'evi': 0.28},
        {'emotions': {'neutral': 0.1842, 'anger': 0.0939, 'disgust': 0.1538, 'joy': 0.1389, 'fear': 0.1573, 'sadness': 0.1566, 'surprise': 0.1154}, 'evi': 0.83},
        {'emotions': {'neutral': 0.1629, 'anger': 0.1578, 'disgust': 0.1010, 'joy': 0.1207, 'fear': 0.1698, 'sadness': 0.1687, 'surprise': 0.1190}, 'evi': 0.49},
        {'emotions': {'neutral': 0.1421, 'anger': 0.1277, 'disgust': 0.1711, 'joy': 0.1242, 'fear': 0.1694, 'sadness': 0.1410, 'surprise': 0.1245}, 'evi': 0.6},
        {'emotions': {'neutral': 0.1902, 'anger': 0.1201, 'disgust': 0.1349, 'joy': 0.1287, 'fear': 0.1672, 'sadness': 0.1555, 'surprise': 0.1034}, 'evi': 0.35},
        {'emotions': {'neutral': 0.1345, 'anger': 0.1247, 'disgust': 0.1026, 'joy': 0.1897, 'fear': 0.1783, 'sadness': 0.1584, 'surprise': 0.1118}, 'evi': 0.93},
        {'emotions': {'neutral': 0.1564, 'anger': 0.1429, 'disgust': 0.1143, 'joy': 0.1302, 'fear': 0.1545, 'sadness': 0.1688, 'surprise': 0.1330}, 'evi': 0.48},
        {'emotions': {'neutral': 0.1471, 'anger': 0.1532, 'disgust': 0.1278, 'joy': 0.1337, 'fear': 0.1456, 'sadness': 0.1502, 'surprise': 0.1424}, 'evi': 0.52},
    ]

    create_heatmap(emotions_batch)
"""