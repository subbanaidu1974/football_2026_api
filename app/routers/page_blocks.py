from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import PageBlock
from ..schemas import PageBlock as PageBlockOut, PageBlockCreate, PageBlockUpdate
from ..crud import CRUD

router = APIRouter(prefix="/page-blocks", tags=["page-blocks"])
crud = CRUD[PageBlock, PageBlockCreate, PageBlockUpdate](PageBlock)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[PageBlockOut])
async def list_blocks(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=PageBlockOut, status_code=201)
async def create_block(payload: PageBlockCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{block_id}", response_model=PageBlockOut)
async def get_block(block_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, block_id)

@router.patch("/{block_id}", response_model=PageBlockOut)
async def update_block(block_id:int, payload: PageBlockUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, block_id, payload)

@router.delete("/{block_id}")
async def delete_block(block_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, block_id)
