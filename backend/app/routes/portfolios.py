from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session

from app.models import Portfolio

router = APIRouter()


@router.get("/", response_model=List[Portfolio])
async def get_portfolios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Portfolio))
    items = result.scalars().unique().all()
    return items


@router.get("/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(*,
                          portfolio_id: UUID,
                          session: AsyncSession = Depends(get_session)):
    query = select(Portfolio).where(Portfolio.id == portfolio_id)
    result = await session.execute(query)
    items = result.scalars().unique().one()
    return items


@router.post("/", response_model=Portfolio)
async def create_portfolio(*,
                           session: AsyncSession = Depends(get_session),
                           item: Portfolio):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
