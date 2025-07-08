from fastapi import APIRouter
from app.services.ai.ollama import ask_ollama, ask_ollama_summary, ask_ollama_wisdom
from app.services.ai.ollama import PromptRequest

router = APIRouter()

@router.post("/llm_ask")
async def ask_ollama_endpoint(request: PromptRequest):
    return await ask_ollama(request)

@router.post("/llm_summary")
async def ask_ollama_summary_endpoint(request: PromptRequest):
    return await ask_ollama_summary(request)

@router.post("/llm_wisdom")
async def ask_ollama_wisdom_endpoint(request: PromptRequest):
    return await ask_ollama_wisdom(request)