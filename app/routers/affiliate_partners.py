from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import AffiliatePartner, AffiliateOffer
from ..schemas import AffiliatePartner as PartnerOut, AffiliatePartnerCreate, AffiliatePartnerUpdate, AffiliateOffer as OfferOut
from ..crud import CRUD

router = APIRouter(prefix="/affiliate-partners", tags=["affiliate-partners"])
crud = CRUD[AffiliatePartner, AffiliatePartnerCreate, AffiliatePartnerUpdate](AffiliatePartner)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[PartnerOut])
async def list_partners(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=PartnerOut, status_code=201)
async def create_partner(payload: AffiliatePartnerCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{partner_id}", response_model=PartnerOut)
async def get_partner(partner_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, partner_id)

@router.patch("/{partner_id}", response_model=PartnerOut)
async def update_partner(partner_id:int, payload: AffiliatePartnerUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, partner_id, payload)

@router.delete("/{partner_id}")
async def delete_partner(partner_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, partner_id)

@router.get("/{partner_id}/offers", response_model=list[OfferOut])
async def partner_offers(partner_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AffiliateOffer).where(AffiliateOffer.partner_id == partner_id))
    return list(res.scalars().all())
