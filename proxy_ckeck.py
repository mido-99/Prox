import requests
from queue import Queue
import threading
from bs4 import BeautifulSoup

q = Queue()
valid_proxies = []

with open("nice_proxies.txt", 'r') as f:
    proxies = [p.strip() for p in f.readlines()]
    for p in proxies:
        q.put(p.strip())

def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            r2 = requests.get('https://quotes.toscrape.com/', 
                              proxies={'http': proxy, 'https': proxy}, 
                              timeout=8)
            if r2.status_code == 200:
                print(f"Valid proxy: {proxy}")
                soup = BeautifulSoup(r2.text, 'lxml')
                quotes = [quote.text for quote in soup.select('span.text')]
                print(quotes)
                valid_proxies.append(proxy)
            else:
                print(f"Failed with status code {r2.status_code}: {proxy}")
        except requests.exceptions.ConnectTimeout:
            print(f"Proxy timed out: {proxy}")
        except requests.exceptions.ProxyError as e:
            print(f"Proxy error: {proxy} with error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {proxy} with error: {e}")
        finally:
            q.task_done()

for _ in range(10):  # Increase number of threads for faster processing
    threading.Thread(target=check_proxy).start()

q.join()  # Wait for all threads to complete

print("Valid proxies:", valid_proxies)
