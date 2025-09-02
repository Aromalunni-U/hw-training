import requests
import logging
from pymongo import MongoClient
from settings import HEADERS, DB_NAME, MONGO_URI, MONGO_COLLECTION_CATEGORY
from mongoengine import connect
from pullandbear_items import ProductDataItem, FailedItem


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]

    def start(self):
        
        for category_data in self.category_collection.find():
            category_id = category_data.get("category_id","")        
            
            params = {
                'languageId': '-1',
                'showProducts': 'false',
                'priceFilter': 'true',
                'appId': '1',
            }
            
            
            product_id_api =  f"https://www.pullandbear.com/itxrest/3/catalog/store/25009531/20309454/category/{category_id}/product"

            
            response = requests.get(
                url = product_id_api,
                params = params,
                headers = HEADERS
            )
            
            if response.status_code == 200:

                data = response.json()

                product_ids = data.get("productIds", [])
                
                item = {}
                
                for product_id in product_ids:
                    
                    item["product_id"] = product_id
                    item["category_id"] = category_id
                    
                    logging.info(item)
                    
                    try:
                        ProductDataItem(**item).save()
                    except:
                        pass
   
            else:
                logging.info(f"Status code : {response.status_code}")
                FailedItem(url = product_id_api, source = "crawler").save()
    


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()