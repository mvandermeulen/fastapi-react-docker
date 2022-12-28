from uuid import UUID

import pytest
from app.tests.utils import create_random_broker
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

# https://github.com/tiangolo/sqlmodel/issues/189
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


@pytest.mark.anyio
async def test_create_item(
        client: AsyncClient
) -> None:
    data = {"name": "Foo"}
    response = await client.post(
        "/api/brokers/", json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


@pytest.mark.anyio
async def test_read_item(
        client: AsyncClient,
        session: AsyncSession
) -> None:
    item = await create_random_broker(session)
    response = await client.get(
        f"/api/brokers/{item.id}"
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == item.name
    assert UUID(content["id"]) == item.id
