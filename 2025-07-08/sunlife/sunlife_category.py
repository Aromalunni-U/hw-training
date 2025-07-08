import requests
from settings import BASE_URL, HEADERS, MONGO_URI, DB_NAME
import logging
from parsel import Selector
from mongoengine import connect
from sunlif_items import CategoryItem, FailedItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        response = requests.get(BASE_URL,headers=HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)
            catefory_url = sel.xpath('//a[@class="catname smaller"]/@href').getall()

            for url in catefory_url:
                response = requests.get(url=url, headers= HEADERS)
                if response.status_code == 200:
                    sel = Selector(response.text)
                    sub_category = sel.xpath('//p[@class="heading-card pb-30"]/a/@href').getall()
                    for sub_url in sub_category:
                        logging.info(sub_url)
                        CategoryItem(url = sub_url).save()
                else:
                    FailedItem(url, source = "category").save()

if __name__ == "__main__":
    category = Category()
    category.start()

