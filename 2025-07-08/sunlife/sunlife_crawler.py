import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME, MONGO_COLLECTION_CATEGORY
from sunlif_items import ProductItem, FailedItem
from mongoengine import connect
from pymongo import MongoClient



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
    
    def start(self):
        for category_data in self.category_collection.find():
            category_name = category_data.get("name","")

            page_no = 1
    
            logging.info(f"{'#'*20} {category_name} {'#'*20}")

            while True:
                
                api_url = "https://nm61sop7f5thlwecp.a1.typesense.net/multi_search?x-typesense-api-key=tSKaWnwrBRsMZnIGKLFCxNDM3qS7ChXz"

                payload = f'''
                    {{
                    "searches": [
                        {{
                        "query_by": "name,sku",
                        "sort_by": "is_out_stock:asc,in_promo:desc,name:asc",
                        "highlight_full_fields": "name,sku",
                        "collection": "ec_products",
                        "q": "*",
                        "facet_by": "brand,categories,offer_label_en,price",
                        "filter_by": "categories:=[{category_name}]",
                        "max_facet_values": 50,
                        "page": {page_no}
                        }}
                    ]
                    }}
                    '''    
                response = requests.post(url=api_url, data=payload, headers=HEADERS)
                if response.status_code == 200:
                    product = self.parse_item(response)
                    if not product:
                        break

                    page_no +=1
                else:
                    logging.error(response.status_code)
                    FailedItem(url = category_data, source = "crawler")

            
    def parse_item(self, response):
        
        data = response.json()
        products = data.get("results",[])[0].get("hits",[])
        if not products:
            return False

        for product in products:
            product_data = product.get("document",{})
            
            pdp_url = product_data.get("url", "")
            product_name  = product_data.get("name", "")
            sales_price = product_data.get("sale_price", "")
            mrp = product_data.get("price", "")
            discount = product_data.get("sale_percent", "")
            instock = product_data.get("is_out_stock", "")

            instock = True if (instock == "false" or instock == False) else False
            discount = discount if discount != "0" else ""

            item = {}

            item["pdp_url"] = pdp_url
            item["product_name"] = product_name
            item["sales_price"] = sales_price
            item["mrp"] = mrp
            item["discount"] = discount
            item["instock"] = instock

            logging.info(item)
            try:
                ProductItem(**item).save()
            except:
                pass
        
        return True



if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()