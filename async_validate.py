import httpx
import asyncio
import json
import time

#? Before you start; refresh your proxy list by visiting: https://proxyscrape.com/free-proxy-list
#? as most proxies would be dead by the next time you come here
#? OR you can use this api directly: https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text

semaphore = asyncio.Semaphore(500)
proxy_api = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text'


def load_from_txt_file(filepath: str):
    '''Load & prepare proxies in scheme http://ip:port from proxies.txt'''    

    with open(filepath, 'r') as file:
        content = file.read()
        proxies = [f"http://{str(proxy['ip'])}:{str(proxy['port'])}" for proxy in 
                json.loads(content)['proxies']]
        
    return proxies

def load_from_api(url: str):
    """Load fresh proxies from https://proxyscrape.com/free-proxy-list"""

    r = httpx.get(url)
    raw_proxies = r.text.split('\n')
    proxies = list(map(str.strip, raw_proxies))
    return proxies

async def load_from_api_2():
    """Load fresh proxies from https://geonode.com/free-proxy-list"""
    #! Not reliable. Most proxies are sock & few are https or http
    
    proxies = []
    async with httpx.AsyncClient() as client:
        for i in range(1, 11):
            url = f'https://proxylist.geonode.com/api/proxy-list?limit=500&page={i}&sort_by=lastChecked&sort_type=desc'
            response  = await client.get(url)
            page_data = response.json()['data']
            page_proxies = [
                f"{proxy['protocols'][0]}://{proxy['ip']}:{proxy['port']}" for proxy in page_data \
                    if not proxy['protocols'][0].startswith('socks')
            ]
            proxies.extend(page_proxies)
    return proxies

async def check_proxy(proxy):
    '''Test each proxy against https://ipinfo.io/json'''

    if proxy.startswith('sock'):
        return None
    
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

    # proxies = load_from_txt_file('proxies.txt')
    # proxies =  await load_from_api_2()
    proxies =  load_from_api(proxy_api)
    print('Tasks to be done:', len(proxies))
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

print('Execution time:-', time2 - time1)