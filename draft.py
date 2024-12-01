import requests, httpx
import asyncio
import json

with open('proxies.txt', 'r') as file:
    
    content = file.read()
    proxies = [f"http://{str(proxy['ip'])}:{str(proxy['port'])}" for proxy in 
               json.loads(content)['proxies']]

async def check_proxy(proxy):
    proxies={
        'http://': proxy,
        'https://': proxy,
        }
    
    try:
        async with httpx.AsyncClient(proxies=proxies, timeout=10) as client:
            r = await client.get('http://ipinfo.io/json')
            
            if r.status_code == 200:
                print('Valid: ', proxy, '-----', r.text)
                return proxy
    except:
        print('Error: ', proxy)

async def main():    
    tasks = [check_proxy(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    valid = [proxy for proxy in results if proxy]
    print(valid)

asyncio.run(main())