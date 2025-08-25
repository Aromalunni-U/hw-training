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
        'akacd_PR-bg-www-prod-safeway': '3933566514~rv=87~id=3776cb0f34bf20d617d0988a9ec32b88',
        'ttcsid': '1756111741770::FATnymg3N0y-e3UDJxyZ.5.1756113738440',
        'ttcsid_CEUU933C77UA1PN5K8JG': '1756111741768::AD9x2Z4eJpuesQVAeoTW.4.1756113738730',
        'incap_ses_713_1610353': 'WgQwXwNm6FRSEJ+zIRblCes1rGgAAAAAjtbyy10DgfzXaYTjzPu71A==',
        'nlbi_1610353_2147483392': 'qR1efeQOqmBSaYjh6eNT2gAAAADiz3NcZ4woyVEsSOZh60NV',
        'reese84': '3:nO0IwFOo3eaiOyoXJ26VOw==:XLC9W+D2HbZX/b7jnJBknNn/lLHBBB2tlrx332qdQRpJIMHBUWay4IoPBEFYav6JIHx2DTB5WNNhcCkkokzuBVK0997xXVE+gW1+Edb+9AEHmgNJyNnzVLp0lZQ9JxyQ6vEOfgngIpKIRfUr3rW6UUm5coJLf8kdgnlWq1KQg/Dc3dF++x2Myu4QFzdpraP54pvW3PzEPGB0sHNozcWFYd2+rwLLZ/aYrOLNs8Jp8ZnG3lEOrCsObqBb2x5A3Nmb+VZ6FCSb7xxKbDr8ELjOFanWz1Y9c0IT8GIOyWT4H/+qJPDUQr/NvcLKB0Fsa81EKnUkrBE7E1arLh8En1mJMF+ht6vPeNdCbKNZy3dZaS3pTmnZfrzpl7Cr20eMOMg3d2KHaBplqhYe3W75r5yVMX1PiregjftDpsiGY/kne4cLQhyrHp9jcHfPY5xsl7BlFQ7BOgg3YvTic6fdv+MAONCfX79Tua0C+K4Fvgay+66XWbJxOqqRQ/AutYLO588QfSHjrPp26P76iTK/tx9zV9AOx2LXUvSEbGMnnGP2CsdarE99I1231+AkGE5flzyi:22FSqs4v090xVDzNVU/fPR2GocqxxORaddLAYYbExD8=',
        'visid_incap_1610353': '/AqOfz8BRQauyseCm9AC85QFrGgAAAAAREIPAAAAAAC1zOzLnyNWhQWZ/ai9Pdgz',
        'nlbi_1610353': 'z7rUU9NC1z1kNY6C6eNT2gAAAABxyM6lFt2CT7Pyi4WQHd2z',
        '_ga_DPTH6L3LZ6': 'GS2.1.s1756116511$o2$g0$t1756116511$j60$l0$h0',
        'ACI_S_ECommBanner': 'safeway',
        'abs_gsession': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22default%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2294611%22%2C%22banner%22%3A%22safeway%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22%22%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%7D%7D',
        'ACI_S_abs_previouslogin': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22default%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2294611%22%2C%22banner%22%3A%22safeway%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22%22%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%7D%7D%7D',
        'SWY_SYND_USER_INFO': '%7B%22storeAddress%22%3A%22%22%2C%22storeZip%22%3A%2294611%22%2C%22storeId%22%3A%223132%22%2C%22preference%22%3A%22J4U%22%7D',
        'ACI_S_ECommSignInCount': '0',
        'at_check': 'true',
        'signifyd_sessionId': '86bHf704-f2ae-P6b9-abda-8b18-5d8f7bb_15ad',
        'AMCVS_A7BF3BC75245ADF20A490D4D%40AdobeOrg': '1',
        'AMCV_A7BF3BC75245ADF20A490D4D%40AdobeOrg': '179643557%7CMCIDTS%7C20326%7CMCMID%7C08691341547215285753083618719494671217%7CMCAAMLH-1756721323%7C12%7CMCAAMB-1756721323%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1756123723s%7CNONE%7CvVersion%7C5.5.0',
        'SAFEWAY_MODAL_LINK': '',
        'SWY_SHARED_SESSION_INFO': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2294611%22%2C%22banner%22%3A%22safeway%22%2C%22preference%22%3A%22J4U%22%2C%22Selection%22%3A%22default%22%2C%22wfcStoreId%22%3A%225799%22%2C%22userData%22%3A%7B%7D%2C%22grsSessionId%22%3A%22c02c3921-f717-4428-9be4-959bb90a99b2%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22%22%7D%2C%22J4U%22%3A%7B%22storeId%22%3A%223132%22%2C%22zipcode%22%3A%2294611%22%2C%22userData%22%3A%7B%7D%7D%2C%22SHOP%22%3A%7B%22storeId%22%3A%223132%22%2C%22zipcode%22%3A%2294611%22%2C%22userData%22%3A%7B%7D%7D%7D%7D',
        'mbox': 'PC#b3d944b563804b13a2b2c618537e0a5f.41_0#1819361325|session#0b0aaff41987483e8a4a7b776bc08990#1756118385',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Aug+25+2025+15%3A38%3A47+GMT%2B0530+(India+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=3a395cbb-017a-4a28-9ae7-c67ae370e882&interactionCount=5&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1&intType=3&geolocation=IN%3BKL&AwaitingReconsent=false',
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
        logging.info(link)
        
        data = response.json()
        products = data.get("catalog", {}).get("response", {}).get("docs", {})
        
        if not products:
            return
        
        product = products[0]
        product_name = product.get("name", "")
        selling_price = product.get("price", "")
        regular_price = product.get("basePrice", "")
        image = product.get("imageUrl", "")

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
