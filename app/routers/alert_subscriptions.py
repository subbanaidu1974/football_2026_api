from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import AlertSubscription
from ..schemas import AlertSubscription as AlSubOut, AlertSubscriptionCreate, AlertSubscriptionUpdate
from ..crud import CRUD

router = APIRouter(prefix="/alert-subscriptions", tags=["alert-subscriptions"])
crud = CRUD[AlertSubscription, AlertSubscriptionCreate, AlertSubscriptionUpdate](AlertSubscription)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[AlSubOut])
async def list_alerts(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=AlSubOut, status_code=201)
async def create_alert(payload: AlertSubscriptionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{al_id}", response_model=AlSubOut)
async def get_alert(al_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, al_id)

@router.patch("/{al_id}", response_model=AlSubOut)
async def update_alert(al_id:int, payload: AlertSubscriptionUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, al_id, payload)

@router.delete("/{al_id}")
async def delete_alert(al_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, al_id)
