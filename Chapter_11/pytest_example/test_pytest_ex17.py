import asyncio

import pytest

@pytest.mark.asyncio
async def test_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(asyncio.sleep(1), timeout=0.5)