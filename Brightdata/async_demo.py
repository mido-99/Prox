"""Send asyncronous requests & check their response"""
import httpx, requests
from dotenv import load_dotenv
import asyncio
import os
import datetime

load_dotenv()
host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
passw = os.getenv("passw")
proxy_url = f'http://{user}:{passw}@{host}:{port}'

url = 'https://httpbin.org/ip'

async def main( url: str, number: int):
    """Send given number of requests to given url for proxy testing"""

    async with httpx.AsyncClient(proxy=proxy_url, timeout=5) as client:
        for _ in range(number):
            curr_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            response = await client.get(url)
            
            print(response.json(), curr_time)

# asyncio.run(main(url, 3))