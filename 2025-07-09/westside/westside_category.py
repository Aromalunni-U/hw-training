import requests
from settings import  HEADERS, BASE_URL, MONGO_URI, DB_NAME
import logging
from parsel import Selector
from mongoengine import connect
from westside_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        response = requests.get(BASE_URL, headers = HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)

            link_xpath = '//li/a[contains(@href, "collections")]/@href'
            category_urls = sel.xpath(link_xpath).getall()
            category_urls = [f"https://www.westside.com{url}" for url in category_urls]

            for category_url in category_urls:
                logging.info(category_url)
                try:
                    CategoryItem(url = category_url).save()
                except:
                    pass        

        else:
            logging.info(f"Status code : {response.status_code}")


if __name__ == "__main__":
    category = Category()
    category.start()

