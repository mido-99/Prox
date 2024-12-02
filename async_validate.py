import httpx
import asyncio
import json
import time

#? Before you start; refresh your proxy list by visiting: https://proxyscrape.com/free-proxy-list
#? as most proxies would be dead by the next time you come here


semaphore = asyncio.Semaphore(500)

with open('proxies.txt', 'r') as file:
    '''Load & prepare proxies in scheme http://ip:port from proxies.txt'''    

    content = file.read()
    proxies = [f"http://{str(proxy['ip'])}:{str(proxy['port'])}" for proxy in 
               json.loads(content)['proxies']]

async def check_proxy(proxy):
    '''Test each proxy against https://ipinfo.io/json'''

    async with semaphore:
        proxies={
            'http://': proxy,
            'https://': proxy,
            }
        
        try:
            async with httpx.AsyncClient(proxies=proxies, timeout=10) as client:
                r = await client.get('https://ipinfo.io/json')
                r2 = await client.get('https://httpbin.org/ip')
                r3 = await client.get('http://lumtest.com/myip.json')

                if (r.status_code + r2.status_code + r3.status_code) == 600:
                    print('Valid: ', proxy, '-----', r.text)
                    return proxy
        except:
            print('Error: ', proxy)
            return None


async def main():
    '''Iterate over proxies for testing'''

    tasks = [check_proxy(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    valid = [proxy for proxy in results if proxy]
    print(valid)
    
    if valid:
        with open('valid.txt', 'w') as file:
            file.writelines(f'{line}\n' for line in valid)

time1 = time.perf_counter()
asyncio.run(main())
time2 = time.perf_counter()

print('Execution time: ', time2 - time1)