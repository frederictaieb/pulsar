from transformers import pipeline
from app.utils.txt.split_text import split_text
from app.utils.txt.is_sentence import is_sentence
import numpy as np

def evi_score(emotions: dict, method: str = "entropy") -> float:
    if method == "entropy":
        return evi_entropy(emotions)
    elif method == "max":
        return evi_max(emotions)
    else:
        raise ValueError(f"Unknown method: {method}")

def evi_entropy(emotions: dict) -> float:
    probs = np.array(list(emotions.values()))
    # Évite log(0) → filtre ou remplace les zéros
    probs = probs[probs > 0]

    h = -np.sum(probs * np.log(probs))
    h_max = np.log(len(emotions))  # Entropie max = log(nombre d’émotions)

    evi = 1 - (h / h_max) if h_max > 0 else 0
    return float(evi)

def evi_max(emotions: dict) -> float:
    return max(emotions.values())

class MultipleSentencesError(Exception):
    pass

# Initialisation du modèle de détection d'émotions
emotion_model = pipeline("text-classification", 
                            model="j-hartmann/emotion-english-distilroberta-base", 
                            top_k=None)

def analyze_emotions(text: str, method: str = "entropy") -> dict:
    raw_scores = emotion_model(text)[0]  # modèle retourne [ [ {label, score}, ... ] ]
    emotions = {r["label"].lower(): r["score"] for r in raw_scores}
    evi = evi_score(emotions, method)
    return {
        #"emotions": raw_scores,
        "emotions": emotions,
        "evi": evi
    }

async def ea_sentence(phrase, method="entropy"):
    if not is_sentence(phrase):
        raise MultipleSentencesError("Input must be a single sentence.")
    result = analyze_emotions(phrase, method)
    return {
#        "sentence": phrase,
        **result
    }

async def ea_text(text, method="entropy"):
    result = analyze_emotions(text, method)
    return {
#        "text": text,
        **result
    }

async def ea_text_by_sentence(text, method="entropy"):
    sentences = split_text(text)
    return [
        {
            #"sentence": sentence,
            **analyze_emotions(sentence, method)
        }
        for sentence in sentences
    ]


