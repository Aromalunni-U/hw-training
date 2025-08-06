import requests
import time
from parsel import Selector
import logging
import json
from settings import USER_AGENTS


def parse_item(response, pdp_url):
    sel = Selector(response.text)

    PRODUCT_NAME_XPATH = '//h1/text()'
    REVIEW_XPATH = '//span[@itemprop="reviewCount"]/text()'
    RATING_XPATH = '//div[@class="rating"]/span/text()'
    BREADCRUMB_XPATH = '//li[@class="breadCrumb__item"]/a/span/text()'
    BRAND_XPATH = '//span[@class="productBasicInfo__productMeta-value-item"]/span/text()'
    SELLING_PRICE_XPATH = '//p[@data-testauto="productprice"]/text()'
    REGULAR_PRICE_XPATH = '//p[contains(@class, "price-value-lead-price-old")]/text()'
    JSON_XPATH = '//script[@type="application/ld+json" and contains(text(),"offers")]/text()'

    product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
    review = sel.xpath(REVIEW_XPATH).get()
    rating = sel.xpath(RATING_XPATH).get()
    breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
    brand = sel.xpath(BRAND_XPATH).get()
    selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
    regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
    json_ld = sel.xpath(JSON_XPATH).get()
    
    data = json.loads(json_ld)
    image = data.get("image", "")


    product_name = product_name.strip()
    review = review.strip() if review else ""
    rating = rating.split(":")[-1].split()[0] if rating else ""
    breadcrumb = " > ".join(breadcrumb)
    brand = brand.strip() if brand else ""
    selling_price = selling_price.strip() if selling_price else ""
    regular_price = regular_price.strip() if regular_price else ""

    image = (
        image[0].replace("//www.coop.ch", "",1).split("?")[0]
        if image else ""
    )

    item = {}

    item["pdp_url"] = pdp_url
    item["product_name"] = product_name
    item["review"] = review
    item["rating"] = rating
    item["breadcrumb"] = breadcrumb
    item["brand"] = brand
    item["selling_price"] = selling_price
    item["regular_price"] = regular_price
    item["image"] = image

    logging.info(item)



# url = "https://www.coop.ch/de/lebensmittel/fruechte-gemuese/fruechte/exotische-fruechte/avocados/naturaplan-bio-avocado/p/3465933"
url = "https://www.coop.ch/de/lebensmittel/fruechte-gemuese/fruechte/c/m_0002?page=1#5650092"

session = requests.Session()


for ua in USER_AGENTS:
    headers = {
        'User-Agent': ua,
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
    'datadome': '1~YZyQTI1fW9TJncY9NnIqrboYiuFA4R5wkf2AhJpBj38wDin6UyxI7EZyUUk3Qfu4jRDDJC4G48KGoM4BE9Mqr_O1tSGREzEwP7VfpsKCoGJusDdt2b6MIK5m0TNJZ7'
    }


    response = session.get(url, headers=headers,cookies=cookies,timeout=10)

    if response.status_code == 200:
        sel = Selector((response.text))

        data = sel.xpath("//script[@type='application/ld+json' and contains(text(), '\"ItemList\"')]/text()").get()
        json_data = json.loads(data)

        product_list = json_data.get("itemListElement", [])
        urls = [product.get("url") for product in product_list if product.get("url")]

        pdp_urls = [url.replace(":443", "") for url in urls]

        for url in pdp_urls:

            response = session.get(url, headers=headers,cookies=cookies,timeout=10)

            if response.status_code == 200:
                parse_item(response,url)
            else:
                logging.error(f"Status code: {response.status_code}")

        break

    elif response.status_code == 403:
        time.sleep(2)
    else:
        logging.error(f"Status code: {response.status_code}")
        break

