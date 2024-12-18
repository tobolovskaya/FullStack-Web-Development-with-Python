import asyncio

import pytest


async def fetch_data(url):
    # Імітація асинхронного запиту
    await asyncio.sleep(1)
    return f"Дані з {url}"


@pytest.fixture
async def async_data():
    await asyncio.sleep(0.5)
    return "Асинхронні дані"


@pytest.mark.asyncio
async def test_with_async_fixture(async_data):
    assert await async_data == "Асинхронні дані"


@pytest.mark.asyncio
@pytest.mark.parametrize("url", ["https://example.com", "https://test.com"])
async def test_fetch_multiple(url):
    result = await fetch_data(url)
    assert result == f"Дані з {url}"