import requests
import logging
from mongoengine import connect
from pymongo import MongoClient
from pullandbear_items import ProductItem
from mongoengine.errors import NotUniqueError
from settings import (
    MONGO_URI, DB_NAME, HEADERS,
    CRAWLER_COLLECTION, PARSE_COLLECTION, MONGO_COLLECTION_CATEGORY
)


class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        db = self.client[DB_NAME]
        self.crawler_collection = db[CRAWLER_COLLECTION]
        self.parser_collection = db[PARSE_COLLECTION]
        self.category_collection = db[MONGO_COLLECTION_CATEGORY]
        
        
    def start(self):
        category_ids = self.category_collection.find({}, {"category_id": 1, "_id": 0})
        
        for category_doc in category_ids:
            category_id = category_doc.get("category_id", "")
            
            product_docs = self.crawler_collection.find(
                {"category_id":category_id}, {"product_id": 1, "_id": 0}
            )
            
            product_ids = list({doc.get("product_id", "") for doc in product_docs})

            batch_size = 12

            for i in range(0, len(product_ids), batch_size):
                batch = product_ids[i:i+batch_size]
                
                params = {
                    'languageId': '-1',
                    'productIds': ",".join([str(i) for i in batch]),
                    'categoryId': category_id,
                    'appId': '1',
                }

                response = requests.get(
                    'https://www.pullandbear.com/itxrest/3/catalog/store/25009531/20309454/productsArray',
                    params=params,
                    headers=HEADERS,
                )
                
                if response.status_code == 200:
                    self.parse_item(response, category_id)
                        
                else:
                    logging.error(f"Status code : {response.status_code}")
                
                

    def parse_item(self, response, category_id):
        
        data = response.json()

        products = data.get("products", [])

        for product in products:
            
            try:
                prices = (
                    product.get("bundleProductSummaries", {})[0]
                    .get("detail", {}).get("colors", [{}])[0]
                    .get("sizes", [{}])[0].get("price", "")        
                )
            except:
                continue
            
            pdp_url = product.get("productUrl", "")
            product_id = product.get("id", "")
            product_description = product.get("detail", {}).get("longDescription", "")
            colors = product.get("bundleColors", [])
            product_type = product.get("productType", "")
            
            
            color = [c.get("name", "") for c in colors]
            prices = float(prices) / 100 if prices else 0
            pdp_url = f"https://www.pullandbear.com/ae/{pdp_url}"
            
            item = {}
            
            item["pdp_url"] = pdp_url
            item["prices"] = prices
            item["product_id"] = product_id
            item["product_description"] = product_description
            item["color"] = color
            item["product_type"] = product_type
            
            
            logging.info(item)
            


            try:
                ProductItem(**item).save()
            except NotUniqueError:
                logging.warning(f"Duplicate product : {item['product_id']}\nURL : {pdp_url}")
                
            except:
                pass




if __name__ == "__main__":
    parser = Parser()
    parser.start()
