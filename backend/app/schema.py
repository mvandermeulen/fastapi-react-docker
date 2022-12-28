from typing import Optional

import strawberry
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from strawberry.fastapi import GraphQLRouter
from strawberry.scalars import JSON
from strawberry.schema.types.base_scalars import UUID
from strawberry.types import Info

from app.crud.repo import CRUDRepository
from app.db import get_session
from app.models import Broker as BrokerModel
from app.models import Portfolio as PortfolioModel
from app.types import (Broker, BrokerOutput, CreateBrokerInput,
                       CreatePortfolioInput, DeleteItemInput, Portfolio,
                       PortfolioOutput, UpdateBrokerInput,
                       UpdatePortfolioInput)


@strawberry.type
class Query:
    @strawberry.field
    async def portfolios(
            self,
            info: Info,
            sort: str | None = None,
            start: int | None = None,
            limit: int | None = None,
            where: Optional[JSON] = None
    ) -> list[Portfolio]:
        crud = CRUDRepository(info.context["db"], PortfolioModel, joinload=True)
        items = await crud.get_list(sort, start, limit, where)
        return items

    @strawberry.field
    async def portfolio(self, id: UUID, info: Info) -> Portfolio:
        crud = CRUDRepository(info.context["db"], PortfolioModel, joinload=True)
        item = await crud.get(id)
        return item

    @strawberry.field
    async def brokers(
            self,
            info: Info,
            sort: str | None = None,
            start: int | None = None,
            limit: int | None = None,
            where: Optional[JSON] = None,
    ) -> list[Broker]:
        crud = CRUDRepository(info.context["db"], BrokerModel, joinload=True)
        items = await crud.get_list(sort, start, limit, where)
        return items

    @strawberry.field
    async def broker(self, id: UUID, info: Info) -> Broker:
        crud = CRUDRepository(info.context["db"], BrokerModel, joinload=True)
        item = await crud.get(id)
        return item


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_portfolio(self,
                               input: UpdatePortfolioInput | None,
                               info: Info
                               ) -> Portfolio:
        crud = CRUDRepository(info.context["db"], PortfolioModel)
        item = await crud.update(input.where.id, input.data.__dict__)
        return item

    @strawberry.mutation
    async def delete_portfolio(self,
                               input: DeleteItemInput | None,
                               info: Info
                               ) -> PortfolioOutput:
        crud = CRUDRepository(info.context["db"], PortfolioModel)
        item = await crud.remove(input.where.id)
        return PortfolioOutput(portfolio=item)

    @strawberry.mutation
    async def create_portfolio(self,
                               input: CreatePortfolioInput | None,
                               info: Info
                               ) -> PortfolioOutput:
        crud = CRUDRepository(info.context["db"], PortfolioModel)
        item = await crud.create(input.data.__dict__)
        return PortfolioOutput(portfolio=item)

    @strawberry.mutation
    async def update_broker(self,
                            input: UpdateBrokerInput | None,
                            info: Info
                            ) -> Broker:
        crud = CRUDRepository(info.context["db"], BrokerModel)
        item = await crud.update(input.where.id, input.data.__dict__)
        return item

    @strawberry.mutation
    async def delete_broker(self,
                            input: DeleteItemInput | None,
                            info: Info
                            ) -> BrokerOutput:
        crud = CRUDRepository(info.context["db"], BrokerModel)
        item = await crud.remove(input.where.id)
        return BrokerOutput(broker=item)

    @strawberry.mutation
    async def create_broker(self,
                            input: CreateBrokerInput | None,
                            info: Info
                            ) -> BrokerOutput:
        crud = CRUDRepository(info.context["db"], BrokerModel)
        item = await crud.create(input.data.__dict__)
        return BrokerOutput(broker=item)


async def get_context(
        db: AsyncSession = Depends(get_session),
):
    return {
        "db": db,
    }

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

graphql_router = GraphQLRouter(schema, context_getter=get_context,)
