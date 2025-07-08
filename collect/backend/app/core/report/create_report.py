import logging
from app.utils.logger import logger_init
from app.schemas.schemas import PromptRequest
from app.core.report.process_report import text_preparation, text_to_summary, text_to_wisdom, text_to_emotions

logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_sentences(report):
    return [item["sentence"] for item in report]

def get_emotions(report):
    return [item["emotions"] for item in report]

def get_evi(report):
    return [item["evi"] for item in report]

async def create_report(request: PromptRequest):
    
    current_prompt = PromptRequest(
        model=request.model,
        prompt=request.prompt
    )

    translated_text = await text_preparation(current_prompt.prompt)   
    logger.info(f"Translated text: {translated_text}")

    current_prompt.prompt = translated_text
    
    summary = await text_to_summary(current_prompt)
    logger.info(f"Summary: {summary['response']}")

    wisdom = await text_to_wisdom(current_prompt)
    logger.info(f"Wisdom: {wisdom['response']}")

    emotions = await text_to_emotions(current_prompt.prompt)
    logger.info(f"Emotions: {emotions}")

    return {
        "summary": summary['response'],
        "wisdom": wisdom['response'],
        "emotions": emotions
    }