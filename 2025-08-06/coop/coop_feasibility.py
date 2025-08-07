import requests
from parsel import Selector
import logging
from settings import USER_AGENTS
import json
import random

headers = {
            'User-Agent':random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
        }

cookies = {
    'datadome': 'rA7ZLwGyWNudWI5D0FBfiGFCJr5sZbBTu9DYmInYfKHJeNcjBSn96EZo11W_wu2uKokpbbohd3w_p3bs2fMy0KDCrBVKH_bgtAOsybPSptqlA2l7vt37I3aROsgWxQJO'
}

##################### CRAWLER ####################

url = "https://www.coop.ch/de/lebensmittel/fruechte-gemuese/fruechte/c/m_0002"

session = requests.Session()
while True:

    response = session.get(url=url,headers=headers, cookies=cookies)
    if response.status_code == 200:
        sel = Selector(response.text)
            
        data = sel.xpath("//script[@type='application/ld+json' and contains(text(), '\"ItemList\"')]/text()").get()
        json_data = json.loads(data)

        product_list = json_data.get("itemListElement", [])
        urls = [product.get("url") for product in product_list if product.get("url")]

        pdp_urls = [url.replace(":443", "") for url in urls]

        for url in pdp_urls:
            logging.info(url)
            c+=1

        next_page = sel.xpath('//a[@class="pagination__next"]/@href').get()
        if not next_page:
            break

        url = f"https://www.coop.ch{next_page}"
    else:
        logging.error(f"Status code : {response.status_code}")


##################### PARSER #####################


pdp_url = "https://www.coop.ch/de/lebensmittel/fruechte-gemuese/fruechte/steinobst/zwetschgen/p/3755116"

session = requests.Session()

response = session.get(url=pdp_url, headers=headers, cookies=cookies)
if response.status_code == 200:
    sel = Selector(response.text)

    PRODUCT_NAME_XPATH = '//h1/text()'
    REVIEW_XPATH = '//span[@itemprop="reviewCount"]/text()'
    RATING_XPATH = '//div[@class="rating"]/span/text()'
    BREADCRUMB_XPATH = '//li[@class="breadCrumb__item"]/a/span/text()'
    BRAND_XPATH = '//span[@class="productBasicInfo__productMeta-value-item"]/span/text()'
    SELLING_PRICE_XPATH = '//p[@data-testauto="productprice"]/text()'
    REGULAR_PRICE_XPATH = '//p[contains(@class, "price-value-lead-price-old")]/text()'
    PERCENTAGE_DISCOUNT_XPATH = '//dt[contains(@id, "rebateText")]/text()'
    JSON_XPATH = '//script[@type="application/ld+json" and contains(text(),"offers")]/text()'

    product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
    review = sel.xpath(REVIEW_XPATH).get()
    rating = sel.xpath(RATING_XPATH).get()
    breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
    brand = sel.xpath(BRAND_XPATH).get()
    selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
    regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
    percentage_discount = sel.xpath(PERCENTAGE_DISCOUNT_XPATH).get()
    json_ld = sel.xpath(JSON_XPATH).get()
    
    data = json.loads(json_ld)
    image = data.get("image", "")

    product_id = pdp_url.split("/")[-1]

else:
    logging.error(f"Status code : {response.status_code}")


