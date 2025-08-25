from curl_cffi import requests
import logging
from pymongo import MongoClient
from settings import HEADERS, DB_NAME, MONGO_URI, MONGO_COLLECTION_CATEGORY
from safeway_items import ProductUrlItem, FailedItem
from mongoengine import connect
from parsel import Selector



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
        
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")
            logging.info(category_url)
            
            
            cookies = {
                'reese84': '3:1A8EgKJh40Oqi4fmJPowJg==:9+2e5hevB6FapjhOK+3vZrMbMBSV0SSdPd/U3v9nUS8Ll8Lm/NNO6pLFD5JU4nY3Ke9ksFT9xpBseBXx8Vd/6uQW9BLw3lKoLRmLOjK0dHADsmv9sZgvIwcyapvPrY1rCpc9JGiPf8mf3Mbx5WYrLo90nahWOxvU0AR0mufAEWWp28xUdGKRmRvRpdqG3p8Nwyu4xWeLGRXGc+76W6hfXQZeHhqrq2KEmpGkTY97SWZN1nzFSqelR25ggsJI+MkmVy96fRP0/PTeLG64NQghHrAfU74T+I3NOh3yYFmykEtnJ7sptIvsodvxq/YnrjhGWPcbSdVsc+tLyXchZCimIX5kmBrlor12wbl1OnAEYKUJfh1nhF5uaKxTaYACow33KJFX1cl7fCKNbvmRricEMWtVbEZp+jnxMowuzQyhhgxzAJKVt6C+CnxANj93Cuhsbh07mAuaOvvBvfrI+w4zkVgGrbNA8sDG8WBvOWRsBHppnnKJNE4lJA2+iSRLidbzV9cajbt9g6MxFN5OPbahZO1vf4L5+cqog3wGOqs3JFehC/Szxmma4spbycsTkDbV:KFoj6ucGE19uQjEc8wTyGpi0tvrs49hfGGIbJB7EALU=',
                'abs_gsession': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22default%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2294611%22%2C%22banner%22%3A%22safeway%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22%22%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%7D%7D',
                'SWY_SYND_USER_INFO': '%7B%22storeAddress%22%3A%22%22%2C%22storeZip%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%2C%22preference%22%3A%22J4U%22%7D',
                'SWY_SHARED_SESSION_INFO': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22default%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2294611%22%2C%22banner%22%3A%22safeway%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22%22%2C%22wfcStoreId%22%3A5799%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%7D%7D',
            }
            
            page_no = 1
            

            while True:
                category_url = f"{category_url}?sort=&page={page_no}&loc=2684"
                response = requests.get(url=category_url, headers=HEADERS, cookies=cookies, impersonate="chrome")
                
                if response.status_code == 200:
                    sel = Selector(response.text)
                    pdp_urls = sel.xpath('//a[contains(@href, "/product-details")]/@href').getall()
                    load_more = sel.xpath('//a[contains(text(), "Load more")]/@href').get()
                    
                    if not load_more:
                        break
                    
                    for url in set(pdp_urls):
                        
                        url = f"https://www.safeway.com{url}"
                        logging.info(url)
                        try:
                            ProductUrlItem(url=url).save()
                        except:
                            pass
                    
                    page_no += 1
                elif response.status_code == 404:
                    logging.info("Pagination completed")
                    break  
                else:
                    logging.error(f"Status code : {response.status_code}")
                    FailedItem(url=category_url, source = "crawler").save()
                    break
                    
            
        
        
if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()