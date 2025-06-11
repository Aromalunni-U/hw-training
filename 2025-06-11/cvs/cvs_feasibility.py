from curl_cffi import requests
from parsel import Selector
import re

HEADERS =  {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
}


################################ CRAWLER ##################################

url = "https://www.cvs.com/shop/vitamins/supplements"

response = requests.get(
    url,
    headers=HEADERS,
    impersonate="chrome120",
    timeout=20,
)


if response.status_code == 200:
    sel = Selector(response.text)
    script_txt = sel.xpath('//script[@id="schema-json-ld"]/text()').get()
    urls = re.findall(r'"url"\s*:\s*"([^"]+)"', script_txt)
    print(urls)
    print(len(urls))
else:
    print(response.status_code)

