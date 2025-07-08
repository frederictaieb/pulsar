from fastapi import APIRouter
from app.core.web3.xrp.send_memo import send_memo
from pydantic import BaseModel
from app.utils.logger import logger_init
from app.schemas.xrp_payload import XrpPayload
import logging

logger_init()
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/send_memo")
async def send_memo_endpoint(req: XrpPayload):
    logger.info(f"Preparing to send memo")
    logger.info(f"datetime: {req.timestamp}")
    logger.info(f"latitude: {req.latitude}")
    logger.info(f"longitude: {req.longitude}")
    logger.info(f"ipfs_ea: {req.ipfs_ea}")
    logger.info(f"ipfs_audio: {req.ipfs_audio}")
    logger.info(f"ipfs_shader: {req.ipfs_shader}")
    return await send_memo(req)


