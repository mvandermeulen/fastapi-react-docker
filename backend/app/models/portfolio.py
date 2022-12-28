from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from app.models.base import IDModelMixin, IDRead


if TYPE_CHECKING:  # pragma: no cover
    from .broker import Broker, BrokerRead  # noqa: F401


class PortfolioBase(SQLModel):
    name: str
    broker_id: Optional[UUID]


class Portfolio(IDModelMixin, PortfolioBase, table=True):
    broker_id: Optional[UUID] = Field(
        sa_column=Column('broker_id', GUID(),
                         ForeignKey('broker.id', name='fk_portfolio_broker_id')))

    broker: Optional["Broker"] = Relationship(back_populates="portfolios")


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioRead(IDRead, PortfolioBase):
    pass


class PortfolioUpdate(IDModelMixin, PortfolioBase):
    name: Optional[str] = None
    broker_id: Optional[UUID] = None


class PortfolioReadWithBroker(PortfolioRead):
    broker: Optional["BrokerRead"] = None
