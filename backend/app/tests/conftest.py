import asyncio
from typing import AsyncGenerator

import alembic
import pytest
from alembic.config import Config
from app.db import async_session
from fastapi import FastAPI
from httpx import AsyncClient


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.main import app
    return app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def session() -> AsyncGenerator:
    async with async_session() as session:
        yield session


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers={"Content-Type": "application/json"}
    ) as client:
        yield client
