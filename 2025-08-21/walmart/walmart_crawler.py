import requests
import logging
from pymongo import MongoClient
from settings import HEADERS, DB_NAME, MONGO_URI, CRAWLER_COLLECTION, MONGO_COLLECTION_CATEGORY
from walmart_items import ProductUrlItem, FailedItem
from mongoengine import connect
from urllib.parse import urlparse
from parsel import Selector
import json



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.collection = self.client[DB_NAME][CRAWLER_COLLECTION]
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
        
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")
            print(category_url)
        
            page_no = 1

            url_parts = urlparse(category_url).path.strip("/").split("/")
            url_parts = "&seo=".join(url_parts[1:])

            while page_no <= 25:
                    
                page_url = f"{category_url}&seo={url_parts}&page={page_no}&affinityOverride=default"
                
                response = requests.get(url=page_url, headers=HEADERS)
                if response.status_code == 200:
                    available = self.parse_item(response)
                    if not available:
                        break
                    page_no += 1
                    
                else:
                    
                    logging.error(f"Status code  {response.status_code}")
                    FailedItem(
                        url = category_url,
                        source = "crawler",
                        status_code = response.status_code
                    ).save()
                    break
                

                
    def parse_item(self, response):
        sel = Selector(response.text)
        
        script_data = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        if script_data:
            data = json.loads(script_data)


            search_data = (
                data.get("props", {})
                .get("pageProps", {})
                .get("initialData", {})
                .get("searchResult", {})
            )

            items = search_data.get("itemStacks", [])[0].get("items", [])
            
            for item in items:
                url = item.get("canonicalUrl", "")
                product_name = item.get("name", "")
                image = item.get("imageInfo", {}).get("thumbnailUrl", "")
                
                
                pdp_url = f"https://www.walmart.com{url}"
                image = image.split("?")[0] if image else ""
                
                item = {}
                
                item["url"] = pdp_url
                item["product_name"] = product_name
                item["image"] = image
                
                logging.info(item)
                try:
                    ProductUrlItem(**item).save()
                except:
                    pass
                
            return True
        
        else:
            return False
                
                    



if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()