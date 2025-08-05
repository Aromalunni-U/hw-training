import requests
from settings import HEADERS, cookies, DB_NAME, DATA_COLLECTION, MONGO_URI
from pymongo import MongoClient
import logging


def parse_item(pdp_url, sku):
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][DATA_COLLECTION]
    
    params = {
        'category_id': '5680',
        'hl': 'hu',
    }
    api_url = f"https://auchan.hu/api/v2/products/sku/{sku}"

    response = requests.get(api_url, params=params, cookies=cookies, headers=HEADERS)


    if response.status_code == 200:

        data = response.json()  

        varient = data.get("defaultVariant", {})

        unique_id = data.get("id", "")
        product_name = varient.get("name", "")
        regular_price = varient.get("price", {}).get("net", "")
        selling_price = varient.get("price", {}).get("netDiscounted", "")
        percentage_discount = varient.get("price", {}).get("discountDisplayPercentage", "")
        uom = varient.get("packageInfo", {}).get("packageUnit", "")
        breadcrumb = " > ".join([cat.get("slug", "") for cat in data.get("categories", [])])

        item = {}

        item["unique_id"] = unique_id
        item["product_name"] = product_name
        item["regular_price"] = regular_price
        item["selling_price"] = selling_price
        item["percentage_discount"] = percentage_discount
        item["breadcrumb"] = breadcrumb
        item["pdp_url"] = pdp_url
        item["uom"] = uom

        logging.info(item)
        collection.insert_one(item)
    else:
        logging.error(f"Status code : {response.status_code}")



page_no =  1

while True:
    params = {
        'page': page_no,
        'itemsPerPage': '12',
        'categoryId': '5669',
        'cacheSegmentationCode': '',
        'hl': 'hu',
    }

    response = requests.get('https://auchan.hu/api/v2/cache/products', params=params, headers=HEADERS, cookies=cookies)

    if response.status_code == 200:

        data = response.json()  

        products = data.get("results", [])

        if not products:
            break

        for product in products:
            variant = product.get("defaultVariant", {})
            name = variant.get("name", "")
            sku = variant.get("sku", "")

            name = "-".join(name.lower().split())

            pdp_url = f"https://auchan.hu/shop/{name}.p-{sku}"

            logging.info(pdp_url)
            parse_item(pdp_url, sku)
        
        page_no +=1
        
    else:
        logging.error(f"Status code : {response.status_code}")
