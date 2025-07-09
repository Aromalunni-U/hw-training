import requests
from parsel import Selector
import re
import json
import logging
from settings import  HEADERS, headers, BASE_URL

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

url = "https://www.westside.com/collections/sale-woman-ethnic-wear"
# url = "https://www.westside.com/collections/joggers-shorts-for-men"

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
            "attributes": [],
            "categories": [category_id],  
            "sort": [
                {"field": "relevance", "order": "asc"},
                {"field": f"product_{category_name}_sortOrder:float", "order": "asc"}
            ],
            "page": page_number,
            "type": "DEFAULT",
            "facets": [],
            "getAllVariants": "false",
            "swatch": [{"key": "product_Multi_Variant_Product"}],
            "currency": "USD",
            "productsCount": 50,
            "showOOSProductsInOrder": "true",
            "inStock": ["true"],
            "attributeFacetValuesLimit": 20,
            "searchedKey": "NzhHalJra25ucnVzZThqMmlwemRMYjY5c0Q0VGlQbFc4dTBrZEl3bU43RT0=",
            "boostGroupIds": [7916789137461, 7913982918709, 7916513787957]
        }

        payload = {
            "fW": "yes",
            "filters": json.dumps(filters),
            "group": "categoryPage"
        }
        url = "https://westside-api.wizsearch.in/v1/products/filter"

        response = requests.post(url, headers=headers, json=payload)
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
