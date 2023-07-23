import asyncio
from typing import Dict, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import async_session
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session")
def event_loop():
    yield asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db() -> AsyncSession:
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="module", autouse=True)
async def client() -> Generator:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture(scope="module")
async def superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest_asyncio.fixture(scope="module")
async def normal_user_token_headers(
    client: AsyncClient, db: AsyncSession
) -> Dict[str, str]:
    return await authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
