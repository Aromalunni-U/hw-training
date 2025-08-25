from curl_cffi  import requests
import logging
from mongoengine import connect
from pymongo import MongoClient
from safeway_items import  FailedItem, ProductItem
from settings import MONGO_URI, DB_NAME, HEADERS, CRAWLER_COLLECTION, PARSE_COLLECTION



class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.crawler_collection = self.client[DB_NAME][CRAWLER_COLLECTION]
        self.parser_collection = self.client[DB_NAME][PARSE_COLLECTION]
        
    def start(self):
        links = self.crawler_collection.find()
        
        cookies = {
                'reese84': '3:1A8EgKJh40Oqi4fmJPowJg==:9+2e5hevB6FapjhOK+3vZrMbMBSV0SSdPd/U3v9nUS8Ll8Lm/NNO6pLFD5JU4nY3Ke9ksFT9xpBseBXx8Vd/6uQW9BLw3lKoLRmLOjK0dHADsmv9sZgvIwcyapvPrY1rCpc9JGiPf8mf3Mbx5WYrLo90nahWOxvU0AR0mufAEWWp28xUdGKRmRvRpdqG3p8Nwyu4xWeLGRXGc+76W6hfXQZeHhqrq2KEmpGkTY97SWZN1nzFSqelR25ggsJI+MkmVy96fRP0/PTeLG64NQghHrAfU74T+I3NOh3yYFmykEtnJ7sptIvsodvxq/YnrjhGWPcbSdVsc+tLyXchZCimIX5kmBrlor12wbl1OnAEYKUJfh1nhF5uaKxTaYACow33KJFX1cl7fCKNbvmRricEMWtVbEZp+jnxMowuzQyhhgxzAJKVt6C+CnxANj93Cuhsbh07mAuaOvvBvfrI+w4zkVgGrbNA8sDG8WBvOWRsBHppnnKJNE4lJA2+iSRLidbzV9cajbt9g6MxFN5OPbahZO1vf4L5+cqog3wGOqs3JFehC/Szxmma4spbycsTkDbV:KFoj6ucGE19uQjEc8wTyGpi0tvrs49hfGGIbJB7EALU=',
                'abs_gsession': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22default%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2294611%22%2C%22banner%22%3A%22safeway%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22%22%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%7D%7D',
                'SWY_SYND_USER_INFO': '%7B%22storeAddress%22%3A%22%22%2C%22storeZip%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%2C%22preference%22%3A%22J4U%22%7D',
                'SWY_SHARED_SESSION_INFO': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22default%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2294611%22%2C%22banner%22%3A%22safeway%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22%22%2C%22wfcStoreId%22%3A5799%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%7D%7D',
            }
        
        HEADERS['ocp-apim-subscription-key'] = '6c21edb7bcda4f0e918348db16147431'


        for link in links:
            link = link.get("url","")
            
            bpn = link.split(".")[-2]
            params = {
                'bpn': bpn,
                'banner': 'safeway',
                'storeId': '3132',
                'bannerId': '1',
                'includeProductRating': 'true',
                'realTimeReviewRating': 'true',
                'guest': 'true',
                'includeOffer': 'true',
                'pgm': 'abs',
            }
            api_url = "https://www.safeway.com/abs/pub/xapi/product/v2/pdpdata"
                
            response = requests.get(
                url=api_url,
                headers=HEADERS,
                cookies=cookies,
                params=params,
                impersonate="chrome"
            )
            
            if response.status_code == 200:
                
                self.parse_item(link, response)
                
            else:
                logging.error(response.status_code)
                FailedItem(url=link,source="parser").save()
                
            
    def parse_item(self,link, response):
                
        data = response.json()
        products = data.get("catalog", {}).get("response", {}).get("docs", {})

        product_name = products[0].get("name", "")
        selling_price = products[0].get("price", "")
        regular_price = products[0].get("basePrice", "")
        image = products[0].get("imageUrl", "")

        review_data = data.get("reviewrating", {}).get("summary", [])
        review = review_data[0].get("reviewCount", "")
        rating = review_data[0].get("avgRating", "")

        product_details = products[0].get("productDetail", {}).get("details", [])
        ingredients, instructionforuse, warning = "", "", ""
        
        for detail in product_details:
            if detail.get("header", "") == "Ingredients":
                ingredients = detail.get("value", "")
            if detail.get("header", "") == "Directions":
                instructionforuse = detail.get("value", "")
            if detail.get("header", "") == "Warnings":
                warning = detail.get("value", "")
                
        ingredients = ingredients.strip() if ingredients else ""
        instructionforuse = (
            instructionforuse.replace("\n","").replace("\r", "").strip()
            if instructionforuse else ""
        )
        warning = warning.strip() if warning else ""
        
        item = {}
        
        item["pdp_url"] = link
        item["product_name"] = product_name
        item["selling_price"] = selling_price
        item["regular_price"] = regular_price
        item["review"] = review
        item["rating"] =  rating
        item["warning"] =  warning
        item["ingredient"] = ingredients
        item["instructionforuse"] = instructionforuse
        item["image"] = image
        
        
        logging.info(item)
        try:
            ProductItem(**item).save()
        except:
            pass
        
    




if __name__ == "__main__":
    parser = Parser()
    parser.start()
