from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import Team, Match
from ..schemas import Team as TeamOut, TeamCreate, TeamUpdate, Match as MatchOut
from ..crud import CRUD

router = APIRouter(prefix="/teams", tags=["teams"])
crud = CRUD[Team, TeamCreate, TeamUpdate](Team)

async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[TeamOut])
async def list_teams(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=TeamOut, status_code=201)
async def create_team(payload: TeamCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{team_id}", response_model=TeamOut)
async def get_team(team_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, team_id)

@router.patch("/{team_id}", response_model=TeamOut)
async def update_team(team_id:int, payload: TeamUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, team_id, payload)

@router.delete("/{team_id}")
async def delete_team(team_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, team_id)

@router.get("/{team_id}/matches", response_model=list[MatchOut])
async def team_matches(team_id:int, role: str = Query("any", enum=["any","home","away"]), db: AsyncSession = Depends(get_db)):
    q = select(Match)
    if role == "home":
        q = q.where(Match.home_team_id == team_id)
    elif role == "away":
        q = q.where(Match.away_team_id == team_id)
    else:
        q = q.where(or_(Match.home_team_id == team_id, Match.away_team_id == team_id))
    res = await db.execute(q)
    return list(res.scalars().all())
