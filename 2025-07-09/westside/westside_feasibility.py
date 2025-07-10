import requests
from parsel import Selector
import json
import logging
from settings import  HEADERS, HEADERS, BASE_URL, headers


def get_category_id(raw_data):

    length = len('"Collection View",')
    start = raw_data.find('"Collection View",')
    end = raw_data.find(");")
    data = raw_data[(start + length) : end]

    data = json.loads(data)
    category_id = data.get("Category ID", "")

    return category_id


################### CATEGORY #########################

res = requests.get(BASE_URL, headers=HEADERS)
sel = Selector(res.text)

link_xpath = '//li/a[contains(@href, "collections")]/@href'
category_urls = sel.xpath(link_xpath).getall()
category_urls = [f"https://www.westside.com{url}" for url in category_urls]

#####################  CRAWLER ######################

url = "https://www.westside.com/collections/joggers-shorts-for-men"

res = requests.get(url, headers=HEADERS)
sel = Selector(res.text)

if res.status_code == 200:
    script = sel.xpath('//script[contains(text(), "Category ID")]/text()').get()

    script_data = script.strip()

    category_id = get_category_id(script_data)
    category_name =  url.split("/")[-1]

    logging.info(category_name)
    print(category_id)

    page_number = 1
    
    while True:

        filters = {
            "productsCount": 50,
            "categories": [category_id],  
            "type": "CATEGORY_PAGE",
            "facets": [],
            "getAllVariants": "false",
            "swatch": [{"key": "product_Multi_Variant_Product"}],
            "currency": "INR",
            "sort": [
                {"field": "relevance", "order": "asc"},
                {"field": f"product_{category_name}_sortOrder:float", "order": "asc"}
            ],
            "showOOSProductsInOrder": "true",
            "inStock": [],
            "page": page_number
        }

        payload = {
            "fW": "yes",
            "filters": json.dumps(filters),
            "group": "categoryPage"
        }
        url = "https://westside-api.wizsearch.in/v1/products/filter"

        response = requests.post(url, headers= headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            results = data.get("payload", {}).get("result", [])

            if not results:
                logging.info("No more products found")
                break

            pdp_urls = [product.get("url") for product in results if product.get("url")]
            
            for url in pdp_urls:
                logging.info(url)
                
            page_number += 1

        else:
            logging.error(response.status_code)
            break



################### PARSER ####################


res  = requests.get(url,headers=HEADERS)
sel = Selector(res.text)

PRODUCT_NAME_XPATH = '//div[@class="product__title"]/h1/text()'
REGULAR_PRICE_XPATH = '//span[@class="price-item price-item--regular"]/text()'
BRAND_XPATH = '//div[@class="pdptitle"]/p/text()'
COUNTRY_XPATTH = '//b[contains(text(), "Country Of Origin")]/following-sibling::text()'
PRODUCT_DESCRIPTION_XPATH = '//div[@class="features_discription"][normalize-space()]/p/text()'
CARE_INSTRUCTION_XPATH = '//b[contains(text(), "Care Instruction")]/following-sibling::text()'
MATERIAL_COMPOSITION_XPATH = '//b[contains(text(), "Fabric Composition")]/following-sibling::text()'
CLOTHING_FIT_XPATH = '//b[contains(text(), "Fit")]/following-sibling::text()'
IMAGE_XPATH = '//div[contains(@class, "product__media")]/img/@src'
COLOR_XPATH = '//div[@class="tooltip"]/text()'
BREADCCRUMB_XPATH = '//a[@class="breadcrumbs__link"]/text()'
SKU_XPATH  = '//b[contains(text(), "SKU")]/following-sibling::text()'
SIZE_XPATH ="//label[@class='product_clr_variant' and @id='pdp-variant']/text()"


product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
brand = sel.xpath(BRAND_XPATH).get()
country_of_origin = sel.xpath(COUNTRY_XPATTH).get()
description = sel.xpath(PRODUCT_DESCRIPTION_XPATH).get()
care_instructions = sel.xpath(CARE_INSTRUCTION_XPATH).get()
material_composition = sel.xpath(MATERIAL_COMPOSITION_XPATH).get()
clothing_fit = sel.xpath(CLOTHING_FIT_XPATH).get()
images = sel.xpath(IMAGE_XPATH).getall()
color = sel.xpath(COLOR_XPATH).getall()
breadcrumb = sel.xpath(BREADCCRUMB_XPATH).getall()
sku = sel.xpath(SKU_XPATH).get()
size = sel.xpath(SIZE_XPATH).getall()
