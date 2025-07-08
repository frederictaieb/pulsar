import fasttext

# Télécharger un modèle pré-entraîné (une seule fois)
# Exemple : https://fasttext.cc/docs/en/language-identification.html

model = fasttext.load_model('lid.176.ftz')

def detect_lang(text):
    prediction = model.predict(text)
    label = prediction[0][0]  # ex: '__label__en'
    confidence = prediction[1][0]
    return label.replace('__label__', ''), confidence

lang, conf = detect_lang("This is an example")
print(lang, conf)
