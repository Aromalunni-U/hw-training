import json
import requests
import logging
from mongoengine import connect
from pymongo import MongoClient
from parsel import Selector
from autozone_items import  FailedItem, ProductItem
from settings import MONGO_URI, DB_NAME, HEADERS, CRAWLER_COLLECTION, PARSE_COLLECTION



class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.crawler_collection = self.client[DB_NAME][CRAWLER_COLLECTION]
        self.parser_collection = self.client[DB_NAME][PARSE_COLLECTION]
        
    def start(self):
        links = self.crawler_collection.find()
        
        # urls =  [
        #     "https://www.autozone.com/internal-engine/timing-set/p/sa-gear-timing-set-3dr-98/155774_0_0"
        #     "https://www.autozone.com/batteries-starting-and-charging/alternator/p/duralast-new-alternator-11390n/1484487_0_0",
        #     "https://www.autozone.com/batteries-starting-and-charging/battery/p/duralast-gold-group-size-47-h5-battery-h5-dlg/832330_0_0",
        #     "https://www.autozone.com/motor-oil-and-transmission-fluid/engine-oil/p/valvoline-restore-protect-full-synthetic-engine-oil-0w-20-5-quart/1345769_0_0",
        # ]
         
        for link in links:
            pdp_url = link.get("url","")
        
            response = requests.get(pdp_url, headers=HEADERS)
            
            if response.status_code == 200:
                self.parse_item(pdp_url,response)
            else:
                logging.error(f"Status code : {response.status_code}")
                # FailedItem(url=pdp_url, source = "parser").save()
            
    
    def parse_item(self, link, response):
        sel = Selector(response.text)
        
        NAME_XPATH = '//h1/text()'
        PRICE_XPATH = '//div[@data-testid="price-fragment"]/span[not(@class="sr-only")]//text()'
        SKU_XPATH = '//div[@data-testid="product-sku-number"]/span[2]/text()'
        PART_XPATH = '//div[@data-testid="partNumber-container"]/span[2]/text()'
        BREADCRUMB_XPATH = '//nav[@aria-label="Breadcrumb"]/span/a/text()'
        DESCRIPTION_XPATH = '//div[h2[contains(@data-testid, "product-description")]]/div//text()'
        IMAGE_XPATH = '//div[@data-testid="enlarged-image-box"]//img/@src'
        CONTAINER_SIZE_XPATH = '//div[@class=" az_FW az_kQb"]/text()'
        LD_JSON_XPATH = '//script[@type="application/ld+json" and contains(text(), "Product")]/text()'
        
        
        product_name = sel.xpath(NAME_XPATH).get()
        price = sel.xpath(PRICE_XPATH).getall()
        sku = sel.xpath(SKU_XPATH).get()
        part = sel.xpath(PART_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        product_description = sel.xpath(DESCRIPTION_XPATH).getall()
        image = sel.xpath(IMAGE_XPATH).get()
        container_size = sel.xpath(CONTAINER_SIZE_XPATH).get()
        
        json_data = sel.xpath(LD_JSON_XPATH).get()
        data = json.loads(json_data)
        with open("demo1.json", "w", encoding="utf-8") as file:
           json.dump(data, file, indent=4, ensure_ascii=False)


        instock = data.get("offers", {}).get("availability", "")
        
                                
                
        price = "".join(price).replace("$", "").strip() if price else 0
        sku = sku.strip() if sku else ""
        part = part.strip() if part else ""
        breadcrumb = " > ".join(breadcrumb) if breadcrumb else ""
        product_description = ", ".join(product_description) if product_description else ""
        container_size = container_size.strip() if container_size else ""
        instock = True if instock and instock == "https://schema.org/InStock" else False
        
         
        review, rating = self.parse_review(sku)
        specification = self.parse_specification(response)
        
        item = {}
        
        item["pdp_url"] = link
        item["product_name"] = product_name
        item["selling_price"] = price
        item["sku"] = sku
        item["part"] = part
        item["breadcrumb"] = breadcrumb
        item["rating"] = rating
        item["review"] = review
        item["product_description"] = product_description
        item["container_size"] = container_size
        item["instock"] = instock
        item["image"] = image
        item["specification"] = specification
        
        logging.info(item)
        # try:
        #     ProductItem(**item).save()
        # except:
        #     pass
        
        
    
    def parse_review(self, sku):
        
        params = {
            'skuNumbers': sku,
        }   
        
        api_url = 'https://external-api.autozone.com/sls/product/product-reviews-integration-bs/v1/review-statistics'
        
        review, rating = "", ""
        
        response = requests.get(url=api_url, params=params, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            review_data = data[0]
            if review_data:
                review = review_data.get("totalReviewCount", "")
                rating = review_data.get("averageOverallRating", "")
                
                rating = round(float(rating), 1) if rating else ""
                
            return review, rating
        
        else:
            logging.error(f"Review status code : {response.status_code}")
            return review, rating
    
    
    
    def parse_specification(self, response):
        
        sel = Selector(response.text)
        script = sel.xpath('//script[@type="application/json"]/text()').get()
        data = json.loads(script)
        
        specification = {}
        
        for row in sel.xpath('//tbody/tr'):
            key = row.xpath('./th/text()').get()
            value = row.xpath('./td//text()').getall()
            
            if key:
                specification[key] = "".join(value)
        
            
        
        queries = data.get("props", {}).get("pageProps", {}).get("dehydratedState", {}).get("queries", [])
        
        for query in queries:
            try:
                product = query.get("state",{}).get("data", {}).get("product", {})
            except:
                continue
            if product:
                spec_data = product.get("productAttributes", [])
                for spec in spec_data:
                    specification[spec.get("name")] = spec.get("value")
                break
            
        return specification

            




if __name__ == "__main__":
    parser = Parser()
    parser.start()
