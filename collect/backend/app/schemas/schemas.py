from pydantic import BaseModel
from datetime import datetime

class PromptRequest(BaseModel):
    model: str = "tinyllama"
    prompt: str 

class SharingsPayload(BaseModel):
    latitude: float | None
    longitude: float | None
    data: str
    
class XrpPayload(BaseModel):
    timestamp: datetime = datetime.now()
    latitude: float | None
    longitude: float | None
    ipfs_ea: str
    ipfs_heatmap : str
    ipfs_audio: str