import logging
from datetime import datetime
from app.utils.logger import logger_init
from app.schemas.schemas import SharingsPayload, XrpPayload
from app.core.send_transaction import send_memo
from app.core.report.create_report import create_report
from app.core.report.send_report import send_report
from app.schemas.schemas import PromptRequest
from app.core.vsl.create_heatmap import create_heatmap
from app.core.vsl.send_heatmap import send_heatmap
from app.core.snd.create_audio import create_audio
from app.core.snd.send_audio import send_audio

logger_init()
logger = logging.getLogger(__name__)

async def wormhole(data: SharingsPayload):
    latitude = data.latitude
    longitude = data.longitude
    sharing = data.data

    if not latitude or not longitude or not sharing:
        logger.error(f"Invalid data")
        return {
            "result": "Invalid data"
        }

    logger.info(f"Incoming Data From Wormhole")
    logger.info(f"Latitude: {latitude}")
    logger.info(f"Longitude: {longitude}")
    logger.info(f"Data: {sharing}")

    logger.info(f"Analysis Data")
    #if data is some text
    report = await create_report(PromptRequest(prompt=sharing, model="tinyllama"))
    logger.info(f"Report: {report}")

    logger.info(f"Uploading Report to IPFS")
    ipfs_ea = await send_report(report)
    logger.info(f"CID Report EA: {ipfs_ea}")

    heatmap_path = create_heatmap(report["emotions"])
    logger.info(f"Heatmap: {heatmap_path}")

    logger.info(f"Uploading Heatmap to IPFS")
    ipfs_heatmap = await send_heatmap(heatmap_path)
    logger.info(f"CID Heatmap: {ipfs_heatmap}")
    
    logger.info(f"creating audio")
    audio_base64 = await create_audio(report)

    logger.info(f"Uploading Audio to IPFS")
    ipfs_audio = await send_audio(audio_base64)
    logger.info(f"CID Audio: {ipfs_audio}")
 

    logger.info(f"Preparing transaction")

    xrp_payload = XrpPayload(
        timestamp=datetime.now(),
        latitude=latitude,
        longitude=longitude,
        ipfs_ea=ipfs_ea,
        ipfs_heatmap=ipfs_heatmap,
        ipfs_audio=ipfs_audio,
    )

    logger.info(f"Sending transaction")
    result = await send_memo(xrp_payload)
    logger.info(f"Transaction result: {result}")

    return {
        "result": result
    }


    