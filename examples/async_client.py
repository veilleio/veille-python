"""Use the asyncio client."""

import asyncio

from veille import AsyncVeilleClient


async def main() -> None:
    async with AsyncVeilleClient() as client:  # reads VEILLE_API_KEY
        response = await client.intelligence_email(query="jane.doe@example.com")
        print(response.data)


asyncio.run(main())
