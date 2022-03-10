from aiohttp import ClientSession,Fingerprint
import asyncio

async def fetch(url, session):
    return await session.get(url,ssl=False)

async def run(r):
    url = "https://google.com"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        for r in responses:
            print(r.ok)



asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
res = asyncio.run(run(1))
print(res)

