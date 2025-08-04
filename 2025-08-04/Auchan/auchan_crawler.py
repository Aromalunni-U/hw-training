import requests
from settings import HEADERS, cookies
import logging


def parse_item(pdp_url, sku):
    

    params = {
        'page': '1',
        'itemsPerPage': '1',
        'auchanCodes[]': [sku],
        'filters[]': 'available',
        'filterValues[]': '1',
        'cacheSegmentationCode': '',
        'hl': 'hu',
    }

    response = requests.get('https://auchan.hu/api/v2/cache/products', params=params, headers=HEADERS, cookies=cookies)

    if response.status_code == 200:

        data = response.json()  
        products = data.get("results", [])
        product = products[0] if products else {}

        varient = product.get("defaultVariant", {})

        product_name = varient.get("name", "")
        selling_price = varient.get("price", {}).get("net", "")
        percentage_discount = varient.get("price", {}).get("discountPercentage", "")
        uom = varient.get("packageInfo", {}).get("packageUnit", "")
        breadcrumb = " > ".join([data.get("slug", "") for data in product.get("categories", [])])

        item = {}

        item["product_name"] = product_name
        item["selling_price"] = selling_price
        item["percentage_discount"] = percentage_discount
        item["breadcrumb"] = breadcrumb
        item["pdp_url"] = pdp_url
        item["uom"] = uom

        logging.info(item)
    else:
        logging.error(f"Status code : {response.status_code}")



page_no =  1

while True:
        
    params = {
        'page': page_no,
        'itemsPerPage': '12',
        'categoryId': '5680',
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
