import logging
import re
import json
from parsel import Selector
from curl_cffi import requests
from settings import HEADERS, DB_NAME, MONGO_URI
from mongoengine import connect
from cvs_items import FailedItem, ProductItem


class Parser:
    def __init__(self,pdp_urls):
        connect(DB_NAME, host=MONGO_URI, alias="default")

    def start(self):
        for link in pdp_urls:
            response = requests.get(link,headers=HEADERS)
            if response.status_code == 200:
                logging.info(link)
                self.parse_item(link,response)
            else:
                logging.error(f"Status code: {response.status_code}")
                failed_url = FailedItem(url=link)
                failed_url.save()

    def parse_item(self,url,response):
        response = requests.get(url, headers=HEADERS)

        sel = Selector(response.text)

        PRODUCT_NAME_XPATH = "//h1/text()"
        RATING_XPATH  = '//p[contains(@class,"text-xl")]/text()'
        REVIEW_XPATH = '//p[contains(text(), "reviews")]/text()'
        BREADCRUMB_XPATH = '//nav[@aria-label="breadcrumbs"]//li//span[not(@class="ps-link-leading")]/text()'
        IMAGES_XPATH = '//div[@role="tablist"]/button/img/@src'
        TARGET_SCRIPT_XPATH = '//script[contains(text(), "productData")]/text()'
        JSON_LD_XPATH = '//script[@id="schema-json-ld"]/text()'

        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        rating = sel.xpath(RATING_XPATH).get()
        review = sel.xpath(REVIEW_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        images = sel.xpath(IMAGES_XPATH).getall()
        target_script = sel.xpath(TARGET_SCRIPT_XPATH).get()
        json_ld_text = sel.xpath(JSON_LD_XPATH).get()

        product_data = json.loads(json_ld_text)  
        product = product_data[0]

        currency = product.get('offers',{}).get('priceCurrency')
        product_id = product.get('productID')               
        brand_name = product.get('brand', {}).get('name')


        target_script = target_script.replace("\\n", "").replace("\\", "")
        start = target_script.find('["')
        end = self.find_balanced_json_array(target_script, start)
        data_str = target_script[start:end]
        data_str = self.clean_json_string(data_str)
        
        data = json.loads(data_str)
    
        product_data = data[3]['children'][3].get("productData",[])
        variants = product_data.get("variants",[])[0]
        vendor_content = variants.get("vendorContent",{})
        price_info = product_data.get("defaultVariant",{}).get("priceInfo",{})


        instock = variants.get("inventoryInfo",{}).get("shipInv",{}).get("locationAvailabilityStatus","")
        description_paragraph =  vendor_content.get("vendorDetails",{}).get("vendorDetailsParagraph","")
        description_bullet_point = vendor_content.get("vendorDetails",{}).get("vendorDetailsBullets",[])
        ingredients = vendor_content.get("vendorIngredients",{}).get("vendorIngredientsParagraph","")
        warnings = vendor_content.get("vendorWarning",{}).get("vendorWarningsParagraph","")
        specification = variants.get("dynamicAttributes",{})
        promotion_description = price_info.get("promoDescription","")
        grammage = price_info.get("unitPrice","")
        selling_price = price_info.get("salePrice","")
        orginal_price = price_info.get("listPrice","")

        feeding_recommendation = ""
        if vendor_content.get("vendorDirection"):
            feeding_recommendation = vendor_content["vendorDirection"].get("vendorDirectionsParagraph", "")

        if review:
            review_match = re.search(r'\d+', review)
            review = review_match.group() if review else ""

        instock = True if  instock == "In Stock" else False

        if description_paragraph:
            product_description = f"{description_paragraph}, {', '.join(description_bullet_point)}"
        else:
            product_description = ", ".join(description_bullet_point)

        images = [f"https://www.cvs.com/{img}" for img in images]
        breadcrumb = " > ".join(breadcrumb) if breadcrumb else ""
        promotion_description = promotion_description if promotion_description else ""
        grammage_quantity = grammage.replace("¢","").split("/")[0] if grammage else ""
        grammage_unit = grammage.replace("¢","").replace(".","").split("/")[1] if grammage else ""
        specification = json.dumps(specification) if specification else ""

        item = {}

        item["pdp_url"] = url
        item["product_name"] = product_name
        item["original_price"] = orginal_price
        item["selling_price"] = selling_price
        item["grammage_quantity"] = grammage_quantity
        item["grammage_unit"] = grammage_unit
        item["currency"] = currency
        item["unique_id"] = product_id
        item["breadcrumb"] = breadcrumb
        item["brand"] = brand_name
        item["rating"] = rating
        item["review"] = review
        item["ingredients"] = ingredients
        item["warnings"] = warnings
        item["feeding_recommendation"] = feeding_recommendation
        item["promotion_description"] = promotion_description
        item["product_description"] = product_description
        item["product_specifications"] = specification
        item["images"] = images

        logging.info(item)
        data_item = ProductItem(**item)
        data_item.save()

    def find_balanced_json_array(self, s, start):
        count = 0
        for i in range(start, len(s)):
            if s[i] == '[':
                count += 1
            elif s[i] == ']':
                count -= 1
                if count == 0:
                    return i + 1  

    def clean_json_string(self,data):
        data = re.sub(r':\s*,', ':"",', data)
        while ',,' in data:
            data = data.replace(',,', ',"",')

        data = data.replace('[,', '["",')
        data = data.replace(',]', ',""]')
        data = re.sub(r',(\s*[}\]])', r'\1', data)

        return data



pdp_urls = [
    "https://www.cvs.com/shop/crest-premium-plus-scope-dual-blast-toothpaste-intense-mint-7-2-oz-prodid-637529",
    "https://www.cvs.com/shop/nabisco-lorna-doone-shortbread-cookies-prodid-297958",
    "https://www.cvs.com/shop/tide-simply-all-in-one-liquid-laundry-detergent-refreshing-breeze-24-loads-32-oz-prodid-957802",
    "https://www.cvs.com/shop/off-active-insect-repellent-i-sweat-resistant-prodid-846485"
]

if __name__ == "__main__":
    parser = Parser(pdp_urls=pdp_urls)
    parser.start()

