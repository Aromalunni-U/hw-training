import requests 
import logging
from parsel import Selector
from settings import  MONGO_URI, DB_NAME, BASE_URL, HEADERS
from mongoengine import connect
from safeway_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        
        response = requests.get(url = BASE_URL, headers = HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)
                
            category_links = sel.xpath(
                '//a[@role="menuitem" and not(@aria-haspopup="true")]/@href'
            ).getall()
            
            category_links = [
                f"https://www.safeway.com{link.split("?")[0]}" 
                for link in category_links
                if "/shop/" in link
            ]
            
            for link in category_links:
                logging.info(link)
                try:
                    CategoryItem(url = link).save()
                except:
                    pass
        
        else:
            logging.error(f"Status code: {response.status_code}")



if __name__ == "__main__":
    category = Category()
    category.start()