from curl_cffi import requests
from parsel import Selector  

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8",
    "cache-control": "no-cache",
    "origin": "https://www.rvusa.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.rvusa.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "x-api-key": "4e799501-b8b6-4ef1-bad5-225b3dd1aa8d",
    "x-lm": "0"
}
BASE_URL = "https://www.rvusa.com"


################### CATEGORY #####################

url = "https://www.rvusa.com/rvs-by-type"

res = requests.get(url, headers=HEADERS, impersonate="chrome")
sel = Selector(res.text)

category_url = sel.xpath('//div[@class="selectType__individualContainer"]/a/@href').getall()

category_url = [f"{BASE_URL}{url}" for url in category_url]


################### CRAWLER ######################


currnt_url = "https://www.rvusa.com/travel-trailer-rvs-for-sale?type=travel+trailer"

while currnt_url:
    res = requests.get(currnt_url, headers=HEADERS, impersonate="chrome")

    sel = Selector(res.text)

   
    pdp_urls = sel.xpath('//div[contains(@class, "inventory__unit__container")]/div[1]/a/@href').getall()
    pdp_urls = [f"{BASE_URL}{url}" for url in pdp_urls]

    for url in pdp_urls:
        res = requests.get(url = url, headers=HEADERS, impersonate="chrome")
  
        next_page = sel.xpath('//a[@aria-label="Next"]/@href').get()

        if next_page:
            currnt_url = f"{BASE_URL}{next_page}"
        else:
            break

    
###################### PARSER #########################

url = "https://www.rvusa.com/2024-newmar-4081-class-a-4667296#contact-jump"

res = requests.get(url, headers=HEADERS, impersonate="chrome")

sel = Selector(res.text)

PRICE_XPATH = '//span[contains(@class, "detail-price")]/text()'
PHONE_XPATH = '//a[@title="Call Seller"]/@data-phone'
IMAGE_XPATH = '//img[@itemprop="contentUrl"]/@src'
LOCATION_XPATH = '//div[@class="col-12 col-lg-6 text-center text-md-start mb-2"]/p/text()'
DESCRIPTION_XPATH = '//div[@id="itemdescription"]//text()'
SPEC_ITME_XPATH = '//ul[contains(@class, "detail__unitSpecs__container")]/li'

price = sel.xpath(PRICE_XPATH).get()
phone = sel.xpath(PHONE_XPATH).get()
image = sel.xpath(IMAGE_XPATH).get()
location = sel.xpath(LOCATION_XPATH).getall()
descriptions = sel.xpath(DESCRIPTION_XPATH).getall()
spec_items = sel.xpath(SPEC_ITME_XPATH)


specifications = {}
for item in spec_items:
    key = item.xpath('.//span[contains(@class, "fw-bolder")]/text()').get()
    value = item.xpath('.//span[@class="col-6" or @class="col-6 vinNumber"]//text()').getall()
    if key and key not in ["Price","Sale Price"]:
        specifications[key] = ''.join(value)

description = ' '.join([des.strip() for des in descriptions if des.strip()])

