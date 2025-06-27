import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME, BASE_URL
from parsel import Selector
from almayaonline_items import CategoryItem, FailedItem
from mongoengine import connect

class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        response = requests.get(BASE_URL,headers=HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)
            categories = sel.xpath('//li[@class="all-categories"]/ul/li/a/@href').getall()
            category_urls = [f"{BASE_URL}{url}"  for url in categories]

            for url in category_urls:
                    logging.info(url)
                    category_item = CategoryItem(url=url)
                    category_item.save()
        else:
            logging.error(f"Status code: {response.status_code}")
            failed_item = FailedItem(url=BASE_URL, source="category")
            failed_item.save()

if __name__ == "__main__":
    category = Category()
    category.start()