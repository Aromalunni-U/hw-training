import requests
import logging
import json
from coop_items import  FailedItem, ProductUrlItem
from mongoengine import connect
from pymongo import MongoClient
from parsel import Selector
from settings import (
    MONGO_URI, DB_NAME,
    MONGO_COLLECTION_CATEGORY, headers, cookies
)   


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")

            session = requests.Session()
            logging.info(category_url)

            page_no = 1

            while True:
                url = f"{category_url}?page={page_no}&pageSize=30&q=%3Arelevance&sort=relevance"
                print(url)

                response = session.get(url=url,headers=headers, cookies=cookies)
                if response.status_code == 200:
                    sel = Selector(response.text)

                    data = sel.xpath("//script[@type='application/ld+json' and contains(text(), '\"ItemList\"')]/text()").get()

                    try:
                        json_data = json.loads(data)
                    except Exception as e:
                        break

                    product_list = json_data.get("itemListElement", [])
                    urls = [product.get("url") for product in product_list if product.get("url")]

                    pdp_urls = [url.replace(":443", "") for url in urls]

                    for url in pdp_urls:
                        logging.info(url)
                        try:
                            ProductUrlItem(url = url).save()
                        except:
                            pass
                    page_no += 1

                elif response.status_code == 404:
                    logging.info("Pagination Completed")
                    break
            
                else:
                    FailedItem(url = url, source ="parser").save()
                    logging.error(f"Status code :{response.status_code}")
                    break



if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()