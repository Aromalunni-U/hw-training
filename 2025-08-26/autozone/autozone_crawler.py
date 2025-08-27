from settings import HEADERS
import logging
import requests
from parsel import Selector
from pymongo import MongoClient
from mongoengine import connect
from settings import MONGO_URI, DB_NAME, INTEREXCHANGE_DATA, NO_MATCHED_COLLECTION, cookies
from autozone_items import ProductUrlItem




class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
    
        
    def start(self):
        
        
        part_numbers = self.db[INTEREXCHANGE_DATA].distinct("INTERCHANGE_PART_NUMBER")[:10000]
        
        for number in part_numbers:  
            text = str(number)
            url = f"https://www.autozone.com/searchresult?searchText={text}"

            logging.info(url)
            
            session = requests.Session()
    
            response = session.get(
                url=url, 
                headers=HEADERS,
                cookies=cookies,
                timeout=20
            )
            
            if response.status_code == 200:
                self.parse_item(response, text)

            else:
                logging.error(f"Status code : {response.status_code}")
        
        
    def parse_item(self,response, text):
        
        part_number = str(text)
        found_match = False
        sel = Selector(response.text)
        
        PDP_URL_XPATH = './/a[@class="az_md"]/@href'
        PRODUCT_NAME_XPATH = './/h3/text()'
        SKU_XPATH = './/div[@data-testid="product-sku-number"]/span[@class="az_QSb"]/text()'
        PART_XPATH = './/div[@data-testid="product-part-number"]/span[@class="az_QSb"]/text()'
        CROSS_REF_XPATH = './/div[contains(text(), "Cross-Reference")]/following-sibling::div/text()'
        
        product_card = sel.xpath('//li[@data-testid="product-container"]')
        
        if not product_card:
            self.check_pdp(response, part_number)
            return
        
        for card in product_card:
            
            pdp_url = card.xpath(PDP_URL_XPATH).get()
            product_name = card.xpath(PRODUCT_NAME_XPATH).get()
            sku = card.xpath(SKU_XPATH).get()
            part = card.xpath(PART_XPATH).get()
            cross_reference = sel.xpath(CROSS_REF_XPATH).get()
            
            pdp_url = f"https://www.autozone.com{pdp_url}"
            
            pdp_url = pdp_url if "?" not in pdp_url else "".join(pdp_url.split("?")[0])
            
            sku = sku.strip() if sku else ""
            part = part.strip() if part else ""
            cross_reference = cross_reference.strip() if cross_reference else ""
            
            
            matched = ""
            if sku == part_number:
                matched = "sku"
            elif part == part_number:
                matched = "part"
            elif cross_reference == part_number:
                matched = "cross_reference"
            else:
                continue
            
            found_match = True
            
            item = {}
            
            item["url"] = pdp_url
            item["product_name"] = product_name
            item["sku"] = sku
            item["part"] = part
            item["cross_reference"] = cross_reference
            item["matched"] = matched
            
            logging.info(item)
            
            try:
                ProductUrlItem(**item).save()
            except:
                pass
        
        if not found_match:
            logging.warning(f"No match found : {part_number}")
            self.db[NO_MATCHED_COLLECTION].insert_one({"part_number": part_number})
    
    
    def check_pdp(self, response, part_number):
    
        sel = Selector(response.text)
        
        NAME_XPATH = '//h1/text()'
        SKU_XPATH = '//div[@data-testid="product-sku-number"]/span[2]/text()'
        PART_XPATH = '//div[@data-testid="partNumber-container"]/span[2]/text()'
        
        pdp_url = response.url.split("?")[0]
        product_name = sel.xpath(NAME_XPATH).get() 
        sku = sel.xpath(SKU_XPATH).get()
        part = sel.xpath(PART_XPATH).get()
        
        sku = sku.strip() if sku else ""
        part = part.strip() if part else ""
        
        matched = ""
        if sku == part_number:
            matched = "sku"
        elif part == part_number:
            matched = "part"
        else:
            logging.warning(f"No match found : {part_number}")
            self.db[NO_MATCHED_COLLECTION].insert_one({"part_number": part_number})
            return

        item = {}
                
        item["url"] = pdp_url
        item["product_name"] = product_name
        item["sku"] = sku
        item["part"] = part
        item["cross_reference"] = ""
        item["matched"] = matched
        
        logging.info(item)
        
        try:
            ProductUrlItem(**item).save()
        except:
            pass
            

            
        
if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()