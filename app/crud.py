from __future__ import annotations
from typing import TypeVar, Generic, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

ModelT = TypeVar("ModelT")
CreateS = TypeVar("CreateS")
UpdateS = TypeVar("UpdateS")

class CRUD(Generic[ModelT, CreateS, UpdateS]):
    def __init__(self, model: Type[ModelT]):
        self.model = model

    async def list(self, db: AsyncSession, skip=0, limit=100):
        res = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(res.scalars().all())

    async def get(self, db: AsyncSession, id: int):
        obj = await db.get(self.model, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return obj

    async def create(self, db: AsyncSession, payload: CreateS):
        obj = self.model(**payload.model_dump())
        db.add(obj)
        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, id: int, payload: UpdateS):
        obj = await self.get(db, id)
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, id: int):
        obj = await self.get(db, id)
        await db.delete(obj)
        await db.commit()
        return {"ok": True}
