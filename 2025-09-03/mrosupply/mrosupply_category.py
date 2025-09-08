import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME
from mongoengine import connect
from mrosupply_items import CategoryItem
from parsel import Selector


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.visited = set() 
        
    
    def start(self):
        BASE_URL = "https://www.mrosupply.com/"
        
        response = requests.get(BASE_URL, headers= HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)
            
            first_categories = sel.xpath('//a[@class="cat-name"]/@href').getall()
            first_categories = [f"https://www.mrosupply.com{url}" for url in first_categories]
            
            for url in first_categories:
                self.category_deep_check(url)

        else:
            logging.warning(f"Status code : {response.status_code}")
            
            
            
    def category_deep_check(self, url):
        if url in self.visited:
            return  
        self.visited.add(url)

        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200:

            sel = Selector(res.text)
            subcategories = sel.xpath('//a[@class="absolute_link"]/@href').getall()
            subcategories = [f"https://www.mrosupply.com{url}" for url in subcategories]

            if subcategories:  
                for sub_url in subcategories:
                    self.category_deep_check(sub_url)
            else:  
                try:
                    logging.info(url)
                    CategoryItem(url=url).save()
                except:
                    pass    
                
        else:       
            logging.warning(f"Status code:{res.status_code}")
            return



if __name__ == "__main__":
    category = Category()
    category.start()
