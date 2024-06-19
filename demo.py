import requests

proxy = 'http://200.19.177.120:80'
url = 'https://ipinfo.io/json'

try:
    page = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
    print(page.text)
except requests.RequestException as e:
    print(f"Request failed: {e}")
