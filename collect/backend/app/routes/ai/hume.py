from fastapi import APIRouter
from app.services.ai.hume import synthesize_tts_json, synthesize_tts_wav, TTSRequest

router = APIRouter()

@router.post("/tts_json")
async def synthesize_tts_json_endpoint(request: TTSRequest):
    return await synthesize_tts_json(request)

@router.post("/tts_wav")
async def synthesize_tts_wav_endpoint(request: TTSRequest):
    return await synthesize_tts_wav(request)