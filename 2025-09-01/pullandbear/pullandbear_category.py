import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME
from mongoengine import connect
from pullandbear_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        
    def start(self):
    
        params = {
            'languageId': '-1',
            'typeCatalog': '1',
            'appId': '1',
        }
        
        category_api = 'https://www.pullandbear.com/itxrest/2/catalog/store/25009531/20309454/category'

        response = requests.get(
            url=category_api,
            params=params,
            headers=HEADERS,
        )
        
        if response.status_code == 200:
            self.scrap_catgory_data(response) 
                    
        else:
            logging(f"Status code : {response.status_code}")
            
            
            
    def scrap_catgory_data(self, response):
        
        data = response.json()
        
        categories = data.get("categories", [])[1]
        sub_categories = categories.get("subcategories", [])
        
        
        for category in sub_categories:
            second_sub_categories  = category.get("subcategories", [])
                                        
            for sub_cat in second_sub_categories:   
                category_id = sub_cat.get("id", "")
                category_name = sub_cat.get("name", "")
            
                item = {}
                
                item["category_id"] = category_id
                item["category_name"] = category_name
            
                logging.info(item)
                try:
                    CategoryItem(**item).save()
                except:
                    pass    
    
    
if __name__ == "__main__":
    category = Category()
    category.start()
