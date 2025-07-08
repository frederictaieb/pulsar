from fastapi import APIRouter
from app.services.ai.roberta import ea_sentence, ea_text, ea_text_by_sentence

router = APIRouter()

@router.post("/ea_sentence")
async def ea_sentence_endpoint(sentence: str):
    return await ea_sentence(sentence)

@router.post("/ea_text")
async def ea_text_endpoint(text: str):
    return await ea_text(text)

@router.post("/ea_text_by_sentence")
async def ea_text_by_sentence_endpoint(text: str):
    return await ea_text_by_sentence(text)