import logging
from app.services.ai.hume import synthesize_tts_json, TTSRequest
from app.services.ai.ollama import ask_ollama_narrator, PromptRequest
from app.utils.logger import logger_init
from app.services.ai.gtts import synthesize_gtts, TTSRequest

logger_init()
logger = logging.getLogger(__name__)

async def create_audio(data: dict):
    text_content = data["wisdom"]

    #HUMEAI
    #logger.info(f"Profiling from the text: {text_content}")
    #description = await ask_ollama_narrator(PromptRequest(prompt=text_content))
    #description = "An old wise man with a deep voice and a slow pace, like a voice from the past"
    #logger.info(f"Narrator profile: {description}")
    #tts_request = TTSRequest(text=text_content, description=description["response"])
    #logger.info(f"TTS Request: {tts_request}")
    #result = await synthesize_tts_json(tts_request)

    #GTTS
    result = await synthesize_gtts(TTSRequest(text=text_content))
    return result["audio_base64"]
