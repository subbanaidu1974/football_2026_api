from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import Venue, Match
from ..schemas import Venue as VenueOut, VenueCreate, VenueUpdate, Match as MatchOut
from ..crud import CRUD
from sqlalchemy import select

router = APIRouter(prefix="/venues", tags=["venues"])
crud = CRUD[Venue, VenueCreate, VenueUpdate](Venue)

async def get_db():
    async with async_session() as s:
        yield s

@router.get("/", response_model=list[VenueOut])
async def list_venues(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=VenueOut, status_code=201)
async def create_venue(payload: VenueCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{venue_id}", response_model=VenueOut)
async def get_venue(venue_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, venue_id)

@router.patch("/{venue_id}", response_model=VenueOut)
async def update_venue(venue_id: int, payload: VenueUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, venue_id, payload)

@router.delete("/{venue_id}")
async def delete_venue(venue_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, venue_id)

# relationship: /venues/{id}/matches
@router.get("/{venue_id}/matches", response_model=list[MatchOut])
async def list_venue_matches(venue_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Match).where(Match.venue_id == venue_id))
    return list(res.scalars().all())
