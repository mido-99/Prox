from queue import Queue
import threading
import requests

q = Queue()
valid_proxies = []

with open("proxies_raw.txt", 'r') as f:
    proxies = [p.strip() for p in f.readlines()]
    for p in proxies:
        q.put(p.strip())

def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            r = requests.get('http://ipinfo.io/json',
                            proxies={'http': proxy,
                                    'https': proxy})
            if r.status_code == 200:
                print(proxy)
                print(r.json())
                valid_proxies.append(proxy)
        except:
            continue

for _ in range(6):
    threading.Thread(target=check_proxy).start()
