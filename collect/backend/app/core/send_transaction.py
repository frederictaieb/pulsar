import os
import logging
from dotenv import load_dotenv
from app.utils.logger import logger_init
from xrpl.wallet import Wallet
from app.services.web3.xrp.transaction import send_xrp
from app.schemas.schemas import XrpPayload

logger_init()
logger = logging.getLogger(__name__)

load_dotenv()

async def send_memo(payload: XrpPayload):
    SRC_WALLET_SEED = os.getenv("SRC_SEED")
    DST_WALLET_ADDRESS = os.getenv("DST_ADDR")

    src_wallet = Wallet.from_seed(SRC_WALLET_SEED)
    logger.info(f"Sending data to {DST_WALLET_ADDRESS}")

    res = await send_xrp(src_wallet, DST_WALLET_ADDRESS, 0.00001, payload.json())
    logger.info(f"Transaction sent: {res}")

    return res

