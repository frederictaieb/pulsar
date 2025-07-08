from gtts import gTTS
import base64
import logging
from pydantic import BaseModel
from app.utils.logger import logger_init
import tempfile
import os
import uuid

logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSRequest(BaseModel):
    text: str
    description: str | None = None


#TODO: TEMPORARY IMPLEMENTATION
async def synthesize_gtts(request: TTSRequest):
    tmp_file = None
    generation_id = str(uuid.uuid4())
    try:
        text = request.text
        language = "en"

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang=language)
        tts.save(tmp_file.name)

        with open(tmp_file.name, "rb") as f:
            donnees_audio = f.read()
            audio_base64 = base64.b64encode(donnees_audio).decode('utf-8')

        return {
            "generation_id": generation_id,
            "audio_base64": audio_base64,
            "message": "Success"
        }
    except Exception as e:
        logger.error(f"Error synthesizing audio: {e}")
        return {
            "generation_id": None,
            "audio_base64": None,
            "message": f"Error: {e}"
        }
    finally:
        if tmp_file and os.path.exists(tmp_file.name):
            os.remove(tmp_file.name)
