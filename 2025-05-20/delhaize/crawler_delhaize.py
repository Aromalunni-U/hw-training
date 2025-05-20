from curl_cffi import requests
from parsel import Selector
from settings import BASE_URL, headers, cookies


response = requests.get(
    BASE_URL,
    headers=headers,
    cookies=cookies,
    impersonate="chrome124",
    timeout=30
)
html_path = "2025-05-20/delhaize/delhaize.html"

if response.status_code == 200:
    with open(html_path, "w") as file:
        file.write(response.text)