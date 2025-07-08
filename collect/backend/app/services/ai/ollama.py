from pydantic import BaseModel
from app.utils.txt.clean_text import clean_text
import httpx

class PromptRequest(BaseModel):
    model: str = "tinyllama"
    prompt: str 

async def ask_ollama(data: PromptRequest):
    prompt = clean_text(data.prompt)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post("http://localhost:11434/api/generate", json={
            "model": data.model,
            "prompt": prompt,
            "stream": False
        })
        result = response.json()

    return {
        "model": data.model,
        "prompt": data.prompt,
        "response": result.get("response", "Erreur ou vide")
    }

async def ask_ollama_summary(data: PromptRequest):
    summary_prompt = f"summarizes this text in 3 short sentences. Be neutral, objective and VERY concise. WITHOUT any other text." + data.prompt
    return await ask_ollama(PromptRequest(model=data.model, prompt=summary_prompt))

async def ask_ollama_wisdom(data: PromptRequest, model: str = "tinyllama"):
    wisdom_prompt = f"From the text, write one simple sentence of wisdom. Be neutral, objective and VERY concise. WITHOUT any other text." + data.prompt
    return await ask_ollama(PromptRequest(model=data.model, prompt=wisdom_prompt))

async def ask_ollama_narrator(data: PromptRequest, model: str = "tinyllama"):
    wisdom_prompt = f"""
    In less than 20 words, describe the narrator personnality from the following text in square brackets 
    TEXT : [ """ + data.prompt + " ]"
    return await ask_ollama(PromptRequest(model=data.model, prompt=wisdom_prompt))

