import asyncio

import pytest


async def right_function():
    # Ваш код тут
    await asyncio.sleep(0.3)


async def wrong_function():
    # Ваш код тут
    await asyncio.sleep(1)


@pytest.mark.asyncio
async def test_your_function_completes_in_time():
    try:
        await asyncio.wait_for(right_function(), timeout=0.5)
    except asyncio.TimeoutError:
        pytest.fail("Функція не завершилася вчасно")


@pytest.mark.asyncio
async def test_your_function_doesnt_complete_in_time():
    try:
        await asyncio.wait_for(wrong_function(), timeout=0.5)
    except asyncio.TimeoutError:
        pytest.fail("Функція не завершилася вчасно")