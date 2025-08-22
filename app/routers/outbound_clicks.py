from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import OutboundClick
from ..schemas import OutboundClick as ClickOut, OutboundClickCreate, OutboundClickUpdate
from ..crud import CRUD

router = APIRouter(prefix="/outbound-clicks", tags=["outbound-clicks"])
crud = CRUD[OutboundClick, OutboundClickCreate, OutboundClickUpdate](OutboundClick)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[ClickOut])
async def list_clicks(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=ClickOut, status_code=201)
async def create_click(payload: ClickOut, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{click_id}", response_model=ClickOut)
async def get_click(click_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, click_id)

@router.patch("/{click_id}", response_model=ClickOut)
async def update_click(click_id:int, payload: OutboundClickUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, click_id, payload)

@router.delete("/{click_id}")
async def delete_click(click_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, click_id)
