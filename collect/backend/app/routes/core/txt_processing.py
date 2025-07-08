from fastapi import APIRouter
from app.core.txt_processing import text_preparation, text_to_summary, text_to_wisdom, text_to_emotions
from app.schemas.schemas import PromptRequest

router = APIRouter()

@router.post("/text_preparation")
async def text_preparation_endpoint(txt: str):
    return await text_preparation(txt)

@router.post("/text_to_summary")
async def text_to_summary_endpoint(request: PromptRequest):
    return await text_to_summary(request)

@router.post("/text_to_wisdom")
async def text_to_wisdom_endpoint(request: PromptRequest):
    return await text_to_wisdom(request)

@router.post("/text_to_emotions")
async def text_to_emotions_endpoint(txt: str):
    return await text_to_emotions(txt)