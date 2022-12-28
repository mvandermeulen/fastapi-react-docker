import string
import random

from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Broker


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


async def create_random_broker(
        db: AsyncSession
) -> Broker:
    name = random_lower_string()
    item = Broker(name=name)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
