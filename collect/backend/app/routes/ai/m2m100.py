from fastapi import APIRouter
from app.services.ai.m2m100 import translate_to_english

router = APIRouter()

@router.post("/translate_to_english")
async def translate_to_english_endpoint(text: str):
    return await translate_to_english(text)
