from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import async_session
from ..models import Season, Stage, Match
from ..schemas import Season as SeasonOut, SeasonCreate, SeasonUpdate, Stage as StageOut, Match as MatchOut
from ..crud import CRUD

router = APIRouter(prefix="/seasons", tags=["seasons"])
crud = CRUD[Season, SeasonCreate, SeasonUpdate](Season)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[SeasonOut])
async def list_seasons(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=SeasonOut, status_code=201)
async def create_season(payload: SeasonCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{season_id}", response_model=SeasonOut)
async def get_season(season_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, season_id)

@router.patch("/{season_id}", response_model=SeasonOut)
async def update_season(season_id:int, payload: SeasonUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, season_id, payload)

@router.delete("/{season_id}")
async def delete_season(season_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, season_id)

@router.get("/{season_id}/stages", response_model=list[StageOut])
async def season_stages(season_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Stage).where(Stage.season_id == season_id))
    return list(res.scalars().all())

@router.get("/{season_id}/matches", response_model=list[MatchOut])
async def season_matches(season_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Match).where(Match.season_id == season_id))
    return list(res.scalars().all())
