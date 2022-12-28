from typing import List
from uuid import UUID

from app.crud.repo import CRUDRepository, get_repository
from app.models import Broker, BrokerCreate, BrokerRead, BrokerUpdate
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", response_model=List[BrokerRead])
async def get_brokers(
    crud: CRUDRepository = Depends(get_repository(Broker)),
):
    items = await crud.get_list()
    return items


@router.get("/{item_id}", response_model=BrokerRead)
async def get_broker(
    item_id: UUID,
    crud: CRUDRepository = Depends(get_repository(Broker)),
):
    item = await crud.get(item_id)
    return item


@router.post("/", response_model=BrokerRead)
async def create_broker(
        item: BrokerCreate,
        crud: CRUDRepository = Depends(get_repository(Broker))
):
    item = await crud.create(item.dict(exclude_unset=True))
    return item


@router.put("/", response_model=BrokerRead)
async def update_broker(
        item: BrokerUpdate,
        crud: CRUDRepository = Depends(get_repository(Broker))
):
    item = await crud.update(item.dict(exclude_unset=True))
    return item


@router.delete("/{item_id}", response_model=BrokerRead)
async def delete_broker(
            item_id: UUID,
        crud: CRUDRepository = Depends(get_repository(Broker))
):
    item = await crud.remove(item_id)
    return item
