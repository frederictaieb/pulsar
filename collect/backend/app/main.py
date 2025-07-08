from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ai import hume, ollama, roberta, m2m100, gtts
from app.routes.core import wormhole
from app.utils.logger import logger_init
import logging
from pydantic import BaseModel


logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wormhole.router, prefix="/api/core/wormhole", tags=["Wormhole"])
# Routes API
app.include_router(hume.router, prefix="/api/ai/hume", tags=["Hume - tts"])
app.include_router(gtts.router, prefix="/api/ai/gtts", tags=["GTTS - tts"])
#app.include_router(ollama.router, prefix="/api/ai/ollama", tags=["Ollama - llm"])
#app.include_router(roberta.router, prefix="/api/ai/roberta", tags=["Roberta - ea"])
#app.include_router(m2m100.router, prefix="/api/ai/m2m100", tags=["M2M100 - translation"])
#app.include_router(xrp.router, prefix="/api/web3/xrp", tags=["XRP"])
#app.include_router(txt_processing.router, prefix="/api/core/processing", tags=["Processing"])
#app.include_router(txt_reporting.router, prefix="/api/core/reporting", tags=["Reporting"])

#WebSocket
@app.websocket("/ws")
async def websocket_user(websocket: WebSocket, username: str):
    await websocket_manager(websocket, username)