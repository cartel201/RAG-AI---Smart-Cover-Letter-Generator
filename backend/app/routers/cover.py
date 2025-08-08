import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..services import cover as cover_service
from ..deps import get_embedding, get_vectordb

class CoverReq(BaseModel):
    user_id: str = 'default'
    job_description: str
    tone: str = 'professional'

router = APIRouter(tags=['cover'])

@router.post('/cover-letter')
async def gen_cover(
    req: CoverReq,
    embed=Depends(get_embedding),
    vdb=Depends(get_vectordb),
):
    if not req.job_description.strip():
        raise HTTPException(status_code=400, detail='Job description is required')

    try:
        letter = cover_service.generate(
            req.job_description, req.user_id, req.tone, embed, vdb
        )
        return {'cover_letter': letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
