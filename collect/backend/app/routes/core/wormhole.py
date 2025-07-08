from fastapi import APIRouter
from app.core.wormhole import wormhole
from app.schemas.schemas import SharingsPayload

router = APIRouter()

@router.post("/send_data")
async def wormhole_endpoint(request: SharingsPayload):
    return await wormhole(request)