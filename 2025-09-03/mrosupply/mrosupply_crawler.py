import requests
import logging
from pymongo import MongoClient
from settings import HEADERS, DB_NAME, MONGO_URI, MONGO_COLLECTION_CATEGORY
from mongoengine import connect
from mrosupply_items import ProductUrlItem, FailedItem
from parsel import Selector



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
        
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")
            logging.info(category_url)
            
            page_no = 1

            while True:
                
                url = f"{category_url}?page={page_no}"

                response = requests.get(url=url, headers=HEADERS)
                if response.status_code == 200:
                    sel = Selector(response.text)
                    
                    pdp_urls = sel.xpath('//a[contains(@class, "product-title")]/@href').getall()
                    pdp_urls = [f"https://www.mrosupply.com/{url}" for url in pdp_urls]
                    for url in pdp_urls:
                        logging.info(url)
                        try:
                            ProductUrlItem(url = url).save()
                        except:
                            pass
            
                    page_no += 1
                else:
                    logging.warning(f"Status code : {response.status_code}")
                    break
    
            
    
if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()