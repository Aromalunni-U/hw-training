import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME, CATEGORY_COLLECTION
from pymongo import MongoClient
from mmlafleur_items import FailedItem, ProductUrlItem
from mongoengine import connect
from mongoengine.errors import NotUniqueError


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][CATEGORY_COLLECTION]
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url")
            
            category_name = category_url.split("/")[-1]
            page_no = 1

            while True:
                api_url = f"https://mmlafleur.com/collections/{category_name}?page={page_no}&view=ajax"
                
                response = requests.get(api_url,headers=HEADERS)

                if response.status_code == 200:
                    data = response.json()
                    if data:
                        self.parse_item(data, category_name)
                    else:
                        logging.info(f"Completed : {category_name}")
                        break
                else:
                    logging.error(response.status_code)
                    FailedItem(url = category_url, source ="crawler_api").save()
                
                page_no +=1

    def parse_item(self,data,category_name):
        for item in data:
            for swatch in item.get("swatches",[]):
                url = swatch.get("url","")
                color = swatch.get("color", "")
                product_id = swatch.get("id","")
             
                item = {}

                item["url"] = url
                item["color"] = color
                item["product_id"] = product_id
                item["category"] = category_name
                
                logging.info(item)
                try:
                    data_item = ProductUrlItem(**item)
                    data_item.save()
                except NotUniqueError:
                    logging.warning(f"Duplicate url: {url}")


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()