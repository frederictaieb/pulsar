import os
import dotenv
import tempfile
import base64
import logging

from app.utils.logger import logger_init
from app.services.ipfs.upload import upload_file

dotenv.load_dotenv()

logger_init()
logger = logging.getLogger(__name__)

async def send_audio(audio_base64: str):
    # Décoder le base64 en bytes
    audio_bytes = base64.b64decode(audio_base64)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_bytes)
        temp_file_name = tmp_file.name

    logger.info("Sending audio to IPFS")

    ipfs_url = os.getenv('IPFS_URL')
    cid = upload_file(ipfs_url, temp_file_name)

    # Nettoyage
    os.remove(temp_file_name)

    return cid
