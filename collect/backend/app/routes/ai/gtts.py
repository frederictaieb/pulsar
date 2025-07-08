from fastapi import APIRouter
from app.services.ai.gtts import synthesize_gtts, TTSRequest

router = APIRouter()

@router.post("/gtts_json")
async def synthesize_gtts_endpoint(request: TTSRequest):
    return await synthesize_gtts(request)
