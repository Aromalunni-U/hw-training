import requests
from pymongo import MongoClient
import logging
from settings import MONGO_URI, PARSE_COLLECTION, DB_NAME, CRAWLER_COLLECTION, HEADERS
from urllib.parse import urlparse
from datetime import datetime
import re



class Parser:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.crawler_collection = self.db[CRAWLER_COLLECTION]
        self.parser_collection = self.db[PARSE_COLLECTION]

    def start(self):
        links = self.crawler_collection.find()
        for link in links:
            link = link.get("url")
            path_parts = urlparse(link).path.strip("/").split("/")
            product_code = path_parts[-1]
            slug = path_parts[-2]

            json_url = f"https://www.petsathome.com/_next/data/0cDR4gdEz4ecLbK8jwKl-/en/product/{slug}/{product_code}.json?productId={product_code}&slug={slug}&slug={product_code}"
            response = requests.get(json_url,headers=HEADERS)

            if response.status_code == 200:
                self.parse_iem(link,response)


    def parse_iem(self,url,response):
                
        data = response.json()
        product_details = data.get("pageProps",{}).get("baseProduct",{})
        product_list = product_details.get("products",[{}])
        offers = product_details.get("offerTermsAndConditions", [])
        page_props = data.get("pageProps",{}).get("productRating",{})

        brand = product_details.get("brand","")[0]
        images = product_details.get("imageUrls",[])
        material_composition = product_details.get("composition","")
        product_unique_key = product_details.get("baseProductId","")
        product_name = product_details.get("name","")
        product_description = product_details.get("description","")
        netweight = product_list[0].get("label","")
        price = product_list[0].get("price",{}).get("base","")
        features = product_details.get("featuresAndBenefits",[])
        promotion_description = offers[0].get("header","") if offers else ""
        feeding_recommendation = product_details.get("guides",[{}])[0].get("introduction")
        ingredients = product_details.get("additives",{}).get("analyticalConstituents","")

        if page_props:
            rating = page_props.get("averageRating","") 
            review = page_props.get("reviewCount","")
        else:
            rating = 0
            review = 0

        valid_upto = offers[0].get("body",[])[1] if offers else ""
        if valid_upto:
            match = re.search(
                r"(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4})",
                valid_upto
            )
            valid_upto =  re.sub("st|nd|rd|th", "", match.group())
            dt = datetime.strptime(valid_upto, "%d %B %Y")
            valid_upto = dt.strftime("%Y-%m-%d")

        features = ",".join(features)

        item = {}

        item["pdp_url"] = url
        item["product_name"] = product_name
        item["product_unique_key"] = product_unique_key
        item["regular_price"] = price
        item["brand"] = brand
        item["images"] = images
        item["rating"] = rating
        item["review"] = review
        item["net_weight"] = netweight
        item["valid_upto"] = valid_upto
        item["features"] = features
        item["ingredients"] = ingredients
        item["promotion_description"] = promotion_description
        item["feeding_recommendation"] = feeding_recommendation
        item["material_composition"] = material_composition
        item["product_description"] = product_description

        logging.info(item)
        self.parser_collection.insert_one(item)



parser = Parser()
parser.start()