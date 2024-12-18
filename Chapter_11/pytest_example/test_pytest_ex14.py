import asyncio
import pytest


async def fetch_data(url):
    # Імітація асинхронного запиту
    await asyncio.sleep(1)
    return f"Дані з {url}"


@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("https://example.com")
    assert result == "Дані з https://example.com"