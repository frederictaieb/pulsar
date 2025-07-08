import asyncio
import logging

from app.schemas.schemas import PromptRequest
from app.utils.logger import logger_init

from app.utils.txt.clean_text import clean_text
from app.utils.txt.split_text import split_text

from app.services.ai.m2m100 import translate_to_english
from app.services.ai.ollama import ask_ollama_summary, ask_ollama_wisdom
from app.services.ai.roberta import ea_text_by_sentence

logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)

async def text_preparation(txt: str):
    cleaned_txt = clean_text(txt)
    translated_text = await translate_to_english(cleaned_txt)
    return translated_text

async def text_to_summary(request: PromptRequest):
    summary = await ask_ollama_summary(request)
    return summary

async def text_to_wisdom(request: PromptRequest):
    wisdom = await ask_ollama_wisdom(request)
    return wisdom

async def text_to_emotions(txt: str):
    emotions = await ea_text_by_sentence(txt)
    return emotions