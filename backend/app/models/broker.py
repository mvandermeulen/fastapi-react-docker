from typing import TYPE_CHECKING, List, Optional

from app.models.base import IDModelMixin, IDRead
from sqlmodel import Relationship, SQLModel


if TYPE_CHECKING:  # pragma: no cover
    from .portfolio import Portfolio, PortfolioRead  # noqa: F401


class BrokerBase(SQLModel):
    name: str


class Broker(IDModelMixin, BrokerBase, table=True):
    portfolios: List["Portfolio"] = Relationship(back_populates="broker")


class BrokerCreate(BrokerBase):
    pass


class BrokerRead(IDRead, BrokerBase):
    pass


class BrokerUpdate(IDModelMixin, BrokerBase):
    name: Optional[str] = None


class BrokerReadWithBroker(BrokerRead):
    portfolios:  List["PortfolioRead"] = []
