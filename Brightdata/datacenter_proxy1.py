"""Send a request with Datacenter proxy from BrightData"""
import requests
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
passw = os.getenv("passw")

proxy_url = f'http://{user}:{passw}@{host}:{port}'
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

url = "http://lumtest.com/myip.json"

response = requests.get(url, proxies=proxies, timeout=3)
pprint(response.json())