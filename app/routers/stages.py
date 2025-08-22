from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import async_session
from ..models import Stage, Match
from ..schemas import Stage as StageOut, StageCreate, StageUpdate, Match as MatchOut
from ..crud import CRUD

router = APIRouter(prefix="/stages", tags=["stages"])
crud = CRUD[Stage, StageCreate, StageUpdate](Stage)

async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[StageOut])
async def list_stages(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=StageOut, status_code=201)
async def create_stage(payload: StageCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{stage_id}", response_model=StageOut)
async def get_stage(stage_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, stage_id)

@router.patch("/{stage_id}", response_model=StageOut)
async def update_stage(stage_id:int, payload: StageUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, stage_id, payload)

@router.delete("/{stage_id}")
async def delete_stage(stage_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, stage_id)

@router.get("/{stage_id}/matches", response_model=list[MatchOut])
async def stage_matches(stage_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Match).where(Match.stage_id == stage_id))
    return list(res.scalars().all())
