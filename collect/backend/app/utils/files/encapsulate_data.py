import mimetypes
import magic  # pip install python-magic
import os
from io import BytesIO

def encapsulate_data(data):
    """
    Transforme `data` en une forme standard :
      - Si `data` est un chemin valide -> on le garde tel quel (str)
      - Si `data` est un str sans fichier -> encodé en BytesIO
      - Si `data` est bytes -> BytesIO
      - Si `data` est déjà un BytesIO -> inchangé
    """
    if isinstance(data, str):
        if os.path.exists(data):
            return data  # Chemin de fichier OK
        else:
            return BytesIO(data.encode('utf-8'))  # Texte pur
    elif isinstance(data, bytes):
        return BytesIO(data)
    elif isinstance(data, BytesIO):
        return data
    else:
        raise ValueError(f"Type non pris en charge : {type(data)}")