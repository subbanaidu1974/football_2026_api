from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import Match
from ..schemas import Match as MatchOut, MatchCreate, MatchUpdate
from ..crud import CRUD

router = APIRouter(prefix="/matches", tags=["matches"])
crud = CRUD[Match, MatchCreate, MatchUpdate](Match)

async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[MatchOut])
async def list_matches(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=MatchOut, status_code=201)
async def create_match(payload: MatchCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{match_id}", response_model=MatchOut)
async def get_match(match_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, match_id)

@router.patch("/{match_id}", response_model=MatchOut)
async def update_match(match_id:int, payload: MatchUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, match_id, payload)

@router.delete("/{match_id}")
async def delete_match(match_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, match_id)
