from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import AffiliateOffer, OutboundClick
from ..schemas import AffiliateOffer as OfferOut, AffiliateOfferCreate, AffiliateOfferUpdate, OutboundClick as ClickOut
from ..crud import CRUD

router = APIRouter(prefix="/affiliate-offers", tags=["affiliate-offers"])
crud = CRUD[AffiliateOffer, AffiliateOfferCreate, AffiliateOfferUpdate](AffiliateOffer)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[OfferOut])
async def list_offers(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=OfferOut, status_code=201)
async def create_offer(payload: AffiliateOfferCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{offer_id}", response_model=OfferOut)
async def get_offer(offer_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, offer_id)

@router.patch("/{offer_id}", response_model=OfferOut)
async def update_offer(offer_id:int, payload: AffiliateOfferUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, offer_id, payload)

@router.delete("/{offer_id}")
async def delete_offer(offer_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, offer_id)

@router.get("/{offer_id}/clicks", response_model=list[ClickOut])
async def offer_clicks(offer_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(OutboundClick).where(OutboundClick.offer_id == offer_id))
    return list(res.scalars().all())
