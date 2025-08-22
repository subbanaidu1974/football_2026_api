from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import City, Venue
from ..schemas import City as CityOut, CityCreate, CityUpdate, Venue as VenueOut
from ..crud import CRUD
from sqlalchemy import select

router = APIRouter(prefix="/cities", tags=["cities"])
crud = CRUD[City, CityCreate, CityUpdate](City)

async def get_db():
    async with async_session() as s:
        yield s

@router.get("/", response_model=list[CityOut])
async def list_cities(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=CityOut, status_code=201)
async def create_city(payload: CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{city_id}", response_model=CityOut)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, city_id)

@router.patch("/{city_id}", response_model=CityOut)
async def update_city(city_id: int, payload: CityUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, city_id, payload)

@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, city_id)

# relationship: /cities/{id}/venues
@router.get("/{city_id}/venues", response_model=list[VenueOut])
async def list_city_venues(city_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Venue).where(Venue.city_id == city_id))
    return list(res.scalars().all())
