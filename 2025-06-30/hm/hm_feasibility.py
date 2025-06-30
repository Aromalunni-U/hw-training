import requests
from parsel import Selector
import logging
from settings import HEADERS



################# CRAWLER ###################
 
page_no = 1

while True:
    next_page_url = f"https://www2.hm.com/en_in/women/shop-by-product/tops.html?productTypes=Top&page={page_no}"
    
    logging.info(f"Page: {page_no} - {next_page_url}")

    response = requests.get(next_page_url, headers= HEADERS)
    if response.status_code != 200:
        logging.error(f"Failed : {response.status_code}")
        break

    sel = Selector(response.text)
    pdp_urls = sel.xpath('//div[@class="e4889e"]/a/@href').getall()

    for url in pdp_urls:
        logging.info(url)

    page_no += 1


################### PARSER ####################

url = "https://www2.hm.com/en_in/productpage.1292587001.html"

response = requests.get(url, headers= HEADERS)
sel = Selector(response.text)
print(response)

PRODUCT_NAME_XPATH = '//h1[@class="fe9348 bdb3fa d582fb"]/text()'
REGULAR_PRICE_XPATH = '//span[@class="e70f50 d7cab8 d9ca8b"]/text()'
COMPOSITION_XPATH = '//span[@class="e95b5c f8c1e9 efef57"]/text()'
IMAGE_XPATH = '//ul[@data-testid="grid-gallery"]//img/@src'

product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
material_composition = sel.xpath(COMPOSITION_XPATH).get()
images = sel.xpath(IMAGE_XPATH).getall()

