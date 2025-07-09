import requests
from settings import ajax_url, headers, MONGO_URI, DB_NAME
import logging
from parsel import Selector
from mongoengine import connect
from sunlif_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        response = requests.get(ajax_url, headers=headers)
        if response.status_code == 200:
            sel = Selector(response.text)
            category_blocks = sel.xpath('//div[@class="col"]')

            for block in category_blocks:
                name = block.xpath('.//h6/a/text()').get()
                sub_url = block.xpath('.//h6/a/@href').get()

                if name and sub_url:
                    logging.info(f"{name} - {sub_url}")
                    CategoryItem(url=sub_url, name=name).save()
        else:
            logging.error(f"Status code: {response.status_code}")


if __name__ == "__main__":
    category = Category()
    category.start()

