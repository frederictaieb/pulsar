import pandas as pd
import numpy as np
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
import tempfile
import os
import logging
from app.utils.logger import logger_init

logger_init()
logger = logging.getLogger(__name__)

EMOTION_ORDER = ["neutral", "anger", "disgust", "joy", "fear", "sadness", "surprise"]

EMOTION_COLORS = {
    'joy': '#FFD700',
    'fear': '#483D8B',
    'sadness': '#1E90FF',
    'anger': '#DC143C',
    'disgust': '#556B2F',
    'surprise': '#00CED1',
    'neutral': '#A9A9A9'
}

def hex_to_rgba(hex_color, alpha):
    rgb = mcolors.to_rgb(hex_color)  # tuple (r,g,b) entre 0-1
    rgba = (*rgb, alpha)  # ajoute alpha
    return rgba

def rgba4_to_rgb3(rgba, background=(1, 1, 1)):
    r, g, b, a = rgba
    br, bg, bb = background
    r_blend = (1 - a) * br + a * r
    g_blend = (1 - a) * bg + a * g
    b_blend = (1 - a) * bb + a * b
    return (r_blend, g_blend, b_blend)

def process_data_json(data):
    rows = []
    for i, entry in enumerate(data):
        row = {"index": i, "evi": entry["evi"]}
        row.update(entry["emotions"])  # ajoute chaque émotion comme une colonne
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

def analyze_emotions(df):
    df["dominant"] =       df[EMOTION_ORDER].idxmax(axis=1)
    df["dominant_score"] = df[EMOTION_ORDER].max(axis=1)
    df["dominant_hex"] =   df["dominant"].map(EMOTION_COLORS)
    df["dominant_rgba4"] = df.apply(
        lambda row: hex_to_rgba(row["dominant_hex"], row["evi"]),
        axis=1
    )
    df["dominant_rgba3"] = df.apply(
        lambda row: rgba4_to_rgb3(row["dominant_rgba4"]),
        axis=1
    )
    return df

def emotions_to_colors(df):
    return df["dominant_rgba3"].tolist()

def colors_to_heatmap(list_rgb, resolution=100):
    colors = np.array(list_rgb)  # (N, 3)
    N = colors.shape[0]

    img = np.repeat(colors[:, np.newaxis, :], resolution, axis=1)

    plt.imshow(img, aspect='auto')
    plt.axis('off')

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    tmp_file.close()  # Ferme tout de suite car plt.savefig l'écrira

    plt.savefig(tmp_file.name, bbox_inches='tight', pad_inches=0)
    logging.info(f"Image saved : {tmp_file.name}")
    return tmp_file.name

def create_heatmap(emotions_batch, resolution=100):
    df = process_data_json(emotions_batch)
    df = analyze_emotions(df)
    list_colors = emotions_to_colors(df)
    heatmap_path = colors_to_heatmap(list_colors, resolution)
    return heatmap_path