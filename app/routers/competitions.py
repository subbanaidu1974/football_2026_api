from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import async_session
from ..models import Competition, Season
from ..schemas import Competition as CompetitionOut, CompetitionCreate, CompetitionUpdate, Season as SeasonOut
from ..crud import CRUD

router = APIRouter(prefix="/competitions", tags=["competitions"])
crud = CRUD[Competition, CompetitionCreate, CompetitionUpdate](Competition)

async def get_db():
    async with async_session() as s:
        yield s

@router.get("/", response_model=list[CompetitionOut])
async def list_comp(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=CompetitionOut, status_code=201)
async def create_comp(payload: CompetitionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{comp_id}", response_model=CompetitionOut)
async def get_comp(comp_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, comp_id)

@router.patch("/{comp_id}", response_model=CompetitionOut)
async def update_comp(comp_id:int, payload: CompetitionUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, comp_id, payload)

@router.delete("/{comp_id}")
async def delete_comp(comp_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, comp_id)

@router.get("/{comp_id}/seasons", response_model=list[SeasonOut])
async def comp_seasons(comp_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Season).where(Season.competition_id == comp_id))
    return list(res.scalars().all())
