import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from pytest_httpx import HTTPXMock

from src.core.asgi import get_app
from src.core.dependencies.http import get_httpx_client


@pytest.fixture(scope="session")
def monkey_session() -> Generator[pytest.MonkeyPatch]:
    mp = pytest.MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture
async def httpx_client(httpx_mock: HTTPXMock) -> AsyncGenerator[AsyncClient]:
    _ = httpx_mock
    async with AsyncClient() as client:
        yield client


@pytest.fixture(scope="session")
async def api_client() -> AsyncGenerator[AsyncClient]:
    async def _get_test_async_client() -> AsyncGenerator[AsyncClient]:
        async with AsyncClient() as client:
            yield client

    app = get_app()
    app.dependency_overrides[get_httpx_client] = _get_test_async_client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://0.0.0.0/") as client:
        yield client
