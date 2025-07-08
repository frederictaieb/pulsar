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

async def send_shader(shader_path):
        logger.info(f"Sending shader to IPFS")
        ipfs_url = os.getenv('IPFS_URL')
        cid = upload_file(ipfs_url, shader_path)
        os.remove(shader_path)
        return cid

