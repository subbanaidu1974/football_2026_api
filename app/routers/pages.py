from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models import Page, PageBlock
from ..schemas import Page as PageOut, PageCreate, PageUpdate, PageBlock as PageBlockOut
from ..crud import CRUD

router = APIRouter(prefix="/pages", tags=["pages"])
crud = CRUD[Page, PageCreate, PageUpdate](Page)
async def get_db():
    async with async_session() as s: yield s

@router.get("/", response_model=list[PageOut])
async def list_pages(skip:int=0, limit:int=100, db: AsyncSession = Depends(get_db)):
    return await crud.list(db, skip, limit)

@router.post("/", response_model=PageOut, status_code=201)
async def create_page(payload: PageCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, payload)

@router.get("/{page_id}", response_model=PageOut)
async def get_page(page_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.get(db, page_id)

@router.patch("/{page_id}", response_model=PageOut)
async def update_page(page_id:int, payload: PageUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update(db, page_id, payload)

@router.delete("/{page_id}")
async def delete_page(page_id:int, db: AsyncSession = Depends(get_db)):
    return await crud.delete(db, page_id)

@router.get("/{page_id}/blocks", response_model=list[PageBlockOut])
async def page_blocks(page_id:int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(PageBlock).where(PageBlock.page_id == page_id))
    return list(res.scalars().all())
