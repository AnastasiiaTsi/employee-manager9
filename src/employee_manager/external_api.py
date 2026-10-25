import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"
semaphore = asyncio.Semaphore(3)

async def fetch_one(client: httpx.AsyncClient, url: str, attempts: int = 3) -> dict:
    async with semaphore:
        for attempt in range(1, attempts + 1):
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError):
                if attempt == attempts:
                    raise
                await asyncio.sleep(attempt)
    raise RuntimeError("Unexpected retry state")

async def fetch_statistics_batch(department_ids: list[int]) -> list[dict]:
    urls = [f"{BASE_URL}/departments/{dept_id}/statistics" for dept_id in department_ids]
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [asyncio.create_task(fetch_one(client, url)) for url in urls]
        try:
            results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=10.0)
            return list(results)
        except asyncio.TimeoutError:
            raise