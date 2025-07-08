import os
import logging
from decimal import Decimal

from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment, Memo
from xrpl.asyncio.transaction import autofill_and_sign, submit_and_wait
from xrpl.wallet import Wallet
from xrpl.utils import xrp_to_drops

from app.utils.logger import logger_init

# Init logger
logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example constants for Memo
MEMO_TYPE = "text"
MEMO_FORMAT = "plain/text"

# Get XRPL URL from env
JSON_RPC_URL = os.getenv("TESTNET_URL")


async def send_xrp(sender_wallet: Wallet, destination_address: str, amount_xrp: float, memo: str = None) -> str:
    logger.info(f"Sending {amount_xrp} XRP from {sender_wallet.classic_address} to {destination_address}")

    client = JsonRpcClient(JSON_RPC_URL)

    try:
        # Build base Payment tx
        payment_data = dict(
            account=sender_wallet.classic_address,
            destination=destination_address,
            amount=xrp_to_drops(amount_xrp)
        )

        # Add memo if given
        if memo:
            payment_data["memos"] = [
                Memo(
                    memo_data=memo.encode('utf-8').hex(),
                    memo_type=MEMO_TYPE.encode('utf-8').hex(),
                    memo_format=MEMO_FORMAT.encode('utf-8').hex()
                )
            ]

        payment = Payment(**payment_data)

        # Sign and submit
        signed_tx = await autofill_and_sign(payment, client, sender_wallet)
        response = await submit_and_wait(signed_tx, client)

        tx_id = signed_tx.get_hash()
        logger.info(f"Transaction sent: {tx_id}")
        logger.info(f"Memo: {memo if memo else ''}")

        return tx_id

    except Exception as e:
        logger.error(f"Transaction failed: {e}")
        raise
