import httpx
import asyncio
import json

#? Before you start; refresh your proxy list by visiting: https://proxyscrape.com/free-proxy-list
#? as most proxies would be dead by the next time you come here

with open('proxies.txt', 'r') as file:
    '''Load & prepare proxies in scheme http://ip:port from proxies.txt'''    

    content = file.read()
    proxies = [f"http://{str(proxy['ip'])}:{str(proxy['port'])}" for proxy in 
               json.loads(content)['proxies']]

async def check_proxy(proxy):
    '''Test each proxy against https://ipinfo.io/json'''

    proxies={
        'http://': proxy,
        'https://': proxy,
        }
    
    try:
        async with httpx.AsyncClient(proxies=proxies, timeout=10) as client:
            r = await client.get('https://ipinfo.io/json')
            
            if r.status_code == 200:
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

asyncio.run(main())
