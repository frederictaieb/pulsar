import re
import unicodedata

# Clean text of special characters
def clean_text(text: str) -> str:
    # Remplacement des guillemets typographiques par des guillemets simples
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    # Remplacer les retours à la ligne et tabulations par un espace
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Normaliser les caractères unicode (ex: é → e + ´)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    # Supprimer les caractères spéciaux non désirés (tout sauf lettres, chiffres, ponctuations de base)
    text = re.sub(r"[^a-zA-Z0-9 .,;:!?'\"]+", " ", text) 
    # Réduire les espaces multiples
    text = re.sub(r"\s+", " ", text)
    # Retirer les espaces en début/fin
    text = text.strip()
    return text
    text = text.strip().replace("...", "§ELLIPSIS§")
    return text