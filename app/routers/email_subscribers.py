from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import async_session
from ..models import EmailSubscriber, AlertSubscription
from ..schemas import EmailSubscriber as SubOut, EmailSubscriberCreate, EmailSubscriberUpdate, AlertSubscription as AlSubOut
from ..crud import CRUD

router = APIRouter(prefix="/email-subscribers", tags=["email-subscribers"])
crud = CRUD[EmailSubscriber, EmailSubscriberCreate, EmailSubscriberUpdate](EmailSubscriber)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[SubOut])
async def list_subs(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=SubOut, status_code=201)
async def create_sub(payload: EmailSubscriberCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{sub_id}", response_model=SubOut)
async def get_sub(sub_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, sub_id)

@router.patch("/{sub_id}", response_model=SubOut)
async def update_sub(sub_id:int, payload: EmailSubscriberUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, sub_id, payload)

@router.delete("/{sub_id}")
async def delete_sub(sub_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, sub_id)

@router.get("/{sub_id}/subscriptions", response_model=list[AlSubOut])
async def list_alerts(sub_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AlertSubscription).where(AlertSubscription.subscriber_id == sub_id))
    return list(res.scalars().all())
