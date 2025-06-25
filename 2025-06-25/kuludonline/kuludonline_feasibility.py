import requests
from parsel import Selector
from urllib.parse import urljoin

BASE_URL = "https://kuludonline.com"

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}

response = requests.get(BASE_URL, headers=HEADERS)
sel = Selector(response.text)

category_url = sel.xpath('//li[@class="has-babymenu"]/a/@href').getall()
category_url = [urljoin(BASE_URL, f"{url}-offers") for url in category_url]


# CRAWLER

for url in category_url:
    while True:
        response = requests.get(url=url, headers=HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)
            pdp_urls = sel.xpath('//a[@class="product-item__title"]/@href').getall()
            pdp_urls = [urljoin(BASE_URL, pdp_url) for pdp_url in pdp_urls]

            next_page = sel.xpath('//li[@class="next"]/a/@href').get()
            if not next_page:
                break
            url = urljoin(BASE_URL, next_page)
        else:
            print(response.status_code)
    

# PARSER

url = "https://kuludonline.com/collections/mom-baby-offers/products/novalac-n1-milk-formula-400-gm"


response = requests.get(url, headers=HEADERS)
sel = Selector(response.text)

PRODUCT_NAME_XPATH = '//span[@class="product__title"]/text()'
INSTOCK_XPATH = '//div[contains(@class, "left-quant")]/text()'
DISCOUNT_XPATH = '//span[@class="product-item__badge product-item__badge--sale"]//text()'
SALE_PRICE_XPATH = '//span[@class="price "]/text()'
MRP_XPATH = '//del[@class="product-price--compare"]'


prouct_name = sel.xpath(PRODUCT_NAME_XPATH).get()
instock = sel.xpath(INSTOCK_XPATH).get()
discount = sel.xpath(DISCOUNT_XPATH).get()
sale_price = sel.xpath(SALE_PRICE_XPATH).get()
mrp = sel.xpath(MRP_XPATH).re_first(r'\d+\.\d+')

instock = True if instock.lower().strip() == "in stock" else False

