from typing import Callable, Type
from uuid import UUID

from app.db import get_session
from app.graphql import WhereParser
from fastapi import Depends
from sqlalchemy import JSON
from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDRepository:
    def __init__(self,
                 db: AsyncSession,
                 model: any,
                 joinload: bool = False
                 ) -> None:
        self.db = db
        self.model = model
        self.joinload = joinload

    async def get_list(
        self,
        sort: str | None = None,
        start: int | None = None,
        limit: int | None = None,
        where: JSON | None = None
    ) -> list:

        query = select(self.model)
        if self.joinload:
            query = query.options(joinedload('*'))
        query = WhereParser(self.model, query, sort, start,
                            limit, where).prepare_query()

        result = await self.db.execute(query)
        self.db.expunge_all()
        items = result.scalars().unique().all()

        return items

    async def get(self, item_id: UUID):
        query = select(self.model)
        if self.joinload:
            query = query.options(joinedload('*'))
        query = query.where(self.model.id == item_id)

        result = await self.db.execute(query)
        self.db.expunge_all()
        item = result.scalars().first()

        return item

    async def create(self, item_data: dict):
        item = self.model()
        for key, value in item_data.items():
            setattr(item, key, value)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item_id: UUID, item_data: dict):
        query = select(self.model)
        query = query.where(self.model.id == item_id)

        result = await self.db.execute(query)
        item = result.scalars().unique().one()
        for key, value in item_data.items():
            setattr(item, key, value)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def remove(self,  item_id: UUID):
        query = select(self.model)
        query = query.where(self.model.id == item_id)
        result = await self.db.execute(query)
        item = result.scalars().unique().one()
        await self.db.delete(item)
        await self.db.commit()
        return item


def get_repository(model: any) -> Callable:
    def get_repo(db: AsyncSession = Depends(get_session)) -> CRUDRepository:
        return CRUDRepository(db, model)
    return get_repo
