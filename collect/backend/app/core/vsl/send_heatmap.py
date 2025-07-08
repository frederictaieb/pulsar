import os
import dotenv
import requests
import json
import tempfile

import logging
from app.utils.logger import logger_init
from app.services.ipfs.upload import upload_file

dotenv.load_dotenv()

logger_init()
logger = logging.getLogger(__name__)

async def send_heatmap(heatmap_path):
        logger.info(f"Sending heatmap to IPFS")
        ipfs_url = os.getenv('IPFS_URL')
        cid = upload_file(ipfs_url, heatmap_path)
        os.remove(heatmap_path)
        return cid

