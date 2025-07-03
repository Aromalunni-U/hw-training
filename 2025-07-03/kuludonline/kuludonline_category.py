import requests
from settings import BASE_URL, HEADERS, MONGO_URI, DB_NAME
import logging
from parsel import Selector
from mongoengine import connect
from kuludonline_items import CategoryItem
from urllib.parse import urljoin



class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        response = requests.get(BASE_URL,headers=HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)

            category_urls = sel.xpath('//li[@class="has-babymenu"]/a/@href').getall()
            category_urls = [urljoin(BASE_URL, f"{url}-offers") for url in category_urls]

            for url in category_urls:
                    logging.info(url)
                    category_item = CategoryItem(url=url)   
                    category_item.save()



if __name__ == "__main__":
    category = Category()
    category.start()