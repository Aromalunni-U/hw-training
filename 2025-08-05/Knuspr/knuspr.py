import requests
from parsel import Selector
import logging
import csv
from settings import HEADERS, file_name, FILE_HEADERS


all_items = []

def parse_item(response, pdp_url):

    sel = Selector(response.text)

    PRODUCT_NAME_XPATH = '//h1/a/text()'
    BRAND_XPATH = '//h1/a/p/text()'
    SELLING_PRICE_XPATH = '//span[@data-test="product-price"]/text()'
    GRAMMAGE_XPATH = '//span[@class="detailQuantity"]/text()'
    PRODUCT_DESC_XPATH = '''
        //div[@class="ckContent"]/div[not(@class="autoTranslationAnnouncement")]//p//text() |
        //div[@class="ckContent"]/div[not(@class="autoTranslationAnnouncement")]//text()
    '''
    IMAGE_XPATH = '//div[contains(@class, "sc-c31413-1")]//img/@src'
    COUNTRY_XPATH = '//span[@class="categoryName"]/text()'
    BREADCRUMB_XPATH = '//ul[@data-test="pnlBreadcrumbs"]/li/a/text()'

    product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
    brand = sel.xpath(BRAND_XPATH).get()
    selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
    grammage= sel.xpath(GRAMMAGE_XPATH).get()
    product_description = sel.xpath(PRODUCT_DESC_XPATH).getall()
    image = sel.xpath(IMAGE_XPATH).get()   
    country_of_orgin = sel.xpath(COUNTRY_XPATH).get()
    breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()

    product_id = pdp_url.split("/")[-1].split("-")[0]


    brand = brand.strip() if brand else ""
    selling_price = selling_price.replace("€", "").strip() if selling_price else ""

    if grammage:
        grammage_quantity = grammage.split()[0]
        grammage_unit = grammage.split()[-1]
    else:
        grammage_quantity, grammage_unit , = "", ""

    product_description = " ".join(product_description).replace("\n","").replace("\xa0", "") if product_description else ""
    product_description = product_description.strip() if product_description != "." else ""

    image =  image.split("/https://")[-1]
    image = f"https://{image}"

    breadcrumb = " > ".join(breadcrumb)


    item = {}

    item["pdp_url"] = pdp_url
    item["product_id"] = product_id
    item["product_name"] = product_name
    item["brand"] = brand
    item["selling_price"] = selling_price
    item["grammage_quantity"] = grammage_quantity
    item["grammage_unit"] = grammage_unit
    item["product_description"] = product_description
    item["country_of_orgin"] = country_of_orgin
    item["image"] = image
    item["breadcrumb"] = breadcrumb

    logging.info(item)

    all_items.append(item)



url = "https://www.knuspr.de/en-DE/c4742-glutenfreie-backmischungen"

response = requests.get(url=url, headers=HEADERS)
if response.status_code == 200:
    sel = Selector(response.text)

    pdp_url = sel.xpath('//a[div[@data-test="productCard-body-price"]]/@href').getall()
    pdp_url = [f"https://www.knuspr.de{url}" for url in pdp_url]

    count = 1
    for url in pdp_url:
        if count <= 10:
            response = requests.get(url=url, headers=HEADERS)
            parse_item(response, url)
            count +=1
        else:
            break
else:
    logging.error(f"Status code {response.status_code}")




with open(file_name, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FILE_HEADERS)
    writer.writeheader()
    writer.writerows(all_items)