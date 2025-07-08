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

async def send_report(report):
    logger.info(f"Storing report in temporary json file")
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = os.path.join(tmpdir, "result.json")
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)

        logger.info(f"Sending report to IPFS")
        ipfs_url = os.getenv('IPFS_URL')
        cid = upload_file(ipfs_url, temp_path)
        os.remove(temp_path)
        return cid

