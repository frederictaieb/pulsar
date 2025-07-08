import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import logging
import io

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Couleurs émotions
EMOTION_COLORS = {
    'joy': '#FFD700',
    'fear': '#483D8B',
    'sadness': '#1E90FF',
    'anger': '#DC143C',
    'disgust': '#556B2F',
    'surprise': '#00CED1',
    'neutral': '#A9A9A9'
}

# Ordre fixe
EMOTION_ORDER = list(EMOTION_COLORS.keys())

# Process JSON → long dataframe
def process_data_json(data):
    rows = []
    for i, entry in enumerate(data):
        evi = entry.get("evi", 1.0)
        for label, score in entry["emotions"].items():
            rows.append({
                "index": i,
                "emotion": label,
                "score": score,
                "evi": evi
            })
    df = pd.DataFrame(rows)
    return df

# Pivot → wide format
def analyze_emotions(df):
    pivot = df.pivot(index="index", columns="emotion", values="score").fillna(0)
    pivot["evi"] = df.groupby("index")["evi"].first()
    pivot["dominant"] = pivot[EMOTION_ORDER].idxmax(axis=1)
    return pivot

# Interpolation couleur + alpha
def interpolate_color(color_hex, score, evi, pale_factor=0.8):
    color_rgb = np.array(mcolors.to_rgb(color_hex))
    white_rgb = np.array([1, 1, 1])
    pale_rgb = white_rgb * pale_factor + color_rgb * (1 - pale_factor)
    result_rgb = pale_rgb * (1 - score) + color_rgb * score
    # Renvoie RGBA, alpha = evi (clampé [0,1])
    alpha = max(0, min(1, evi))
    return np.append(result_rgb, alpha)

# Génération heatmap
def text_to_heatmap(emotions, output_path="heatmap.png", to_save=True):
    logger.info(f"*** SHADER: {emotions} ***")

    df_long = process_data_json(emotions)
    df_wide = analyze_emotions(df_long)

    if "dominant" in df_wide.columns:
        data = df_wide.drop(columns=["dominant"])
    else:
        data = df_wide

    evi_series = data.pop("evi")

    emotions = [e for e in EMOTION_ORDER if e in data.columns]
    data = data[emotions]

    n_emotions = len(emotions)
    n_phrases = data.shape[0]

    # RGBA !
    img = np.ones((n_emotions, n_phrases, 4))

    for i, emo in enumerate(emotions):
        color = EMOTION_COLORS.get(emo, '#000000')
        for j in range(n_phrases):
            score = data.iloc[j][emo]
            evi = evi_series.iloc[j]
            img[i, j, :] = interpolate_color(color, score, evi)

    if to_save:
        plt.imsave(output_path, img)
        logging.info(f"Heatmap saved at {output_path}")
        return output_path
    else:
        buffer = io.BytesIO()
        plt.imsave(buffer, img, format='png')
        buffer.seek(0)
        return buffer

# Exemple
if __name__ == "__main__":
    emotions_batch = [
        {'emotions': {'neutral': 0.943, 'surprise': 0.036, 'disgust': 0.007, 'joy': 0.005, 'anger': 0.004, 'sadness': 0.003, 'fear': 0.002}, 'evi': 0.03},
        {'emotions': {'neutral': 0.55, 'anger': 0.20, 'disgust': 0.13, 'joy': 0.046, 'fear': 0.041, 'sadness': 0.025, 'surprise': 0.006}, 'evi': 0.09},
    ]
    text_to_heatmap(emotions_batch, "heatmap_alpha.png")
