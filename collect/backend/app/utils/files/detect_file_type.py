def detect_file_type(file_path_or_bytes, file_name=None):
    """
    Détecte si le fichier est vidéo, audio, texte ou inconnu.
    - file_path_or_bytes : chemin local OU BytesIO.
    - file_name : utile pour deviner l'extension.
    """

    # 1️⃣ Vérifier extension si file_name donné
    ext_type = None
    if file_name:
        _, ext = os.path.splitext(file_name.lower())
        if ext in ['.mp4', '.mkv', '.avi', '.mov', '.flv']:
            ext_type = 'video'
        elif ext in ['.mp3', '.wav', '.aac', '.flac', '.ogg']:
            ext_type = 'audio'
        elif ext in ['.txt', '.md', '.csv', '.log', '.json', '.xml']:
            ext_type = 'text'
    if ext_type:
        return ext_type

    # 2️⃣ Vérifier le MIME type pour un fichier local
    if isinstance(file_path_or_bytes, str):
        mime_type, _ = mimetypes.guess_type(file_path_or_bytes)
    else:
        mime_type = None

    if mime_type:
        if mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('audio/'):
            return 'audio'
        elif mime_type.startswith('text/'):
            return 'text'

    # 3️⃣ Vérifier magic bytes
    if isinstance(file_path_or_bytes, str):
        mime = magic.from_file(file_path_or_bytes, mime=True)
    else:
        mime = magic.from_buffer(file_path_or_bytes.read(2048), mime=True)
        file_path_or_bytes.seek(0)  # Reset le pointeur

    if mime.startswith('video/'):
        return 'video'
    elif mime.startswith('audio/'):
        return 'audio'
    elif mime.startswith('text/'):
        return 'text'
    else:
        return 'unknown'