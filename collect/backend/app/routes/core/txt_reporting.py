from fastapi import APIRouter
from app.core.txt_reporting import text_reporting
from app.schemas.schemas import PromptRequest

router = APIRouter()

@router.post("/text_reporting")
async def text_reporting_endpoint(request: PromptRequest):
    return await text_reporting(request)