"""
Created on Nov 10, 2020

@author: ionut
"""

from typing import TYPE_CHECKING, AsyncIterator

from aiohttp.test_utils import TestClient, TestServer
import pytest_asyncio
from zeus.main import make_app


if TYPE_CHECKING:
    from collections.abc import AsyncIterator


pytest_plugins = "aiohttp.pytest_plugin"


@pytest_asyncio.fixture
async def zeus_server() -> AsyncIterator[TestServer]:
    """Start a single aiohttp test server shared across all tests."""
    app = make_app()
    server = TestServer(app)
    await server.start_server()
    yield server
    await server.close()


@pytest_asyncio.fixture
async def zeus_app(zeus_server) -> AsyncIterator[TestClient]:
    """Create a fresh TestClient per test, reusing the session-scoped server."""
    client = TestClient(zeus_server)
    # return client
    yield client
