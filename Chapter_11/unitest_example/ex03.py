import asyncio
import unittest


async def async_add(a, b):
    await asyncio.sleep(1)
    return a + b


class TestAsyncMethod(unittest.IsolatedAsyncioTestCase):
    async def test_add(self):
        """Add function test"""
        r = await async_add(2, 3)
        self.assertEqual(r, 5)


if __name__ == '__main__':
    unittest.main()