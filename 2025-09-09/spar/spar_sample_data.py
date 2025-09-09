from curl_cffi import requests
from parsel import Selector
from datetime import date
import re
import csv
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}



class Scrape_data:
    def __init__(self):
        self.items = []
        
    def start(self):
        category_names = ["haushalt", "drogerie-beauty", "getraenke"]
        
        for category_name in category_names:
            logging.info(f"{category_name} started ...")
            self.crawler(category_name)
            
        self.to_csv()
    
    def crawler(self, category_name):
        
        api_url = "https://api-scp.spar-ics.com/ecom/pw/v1/search/v1/navigation"
        
        page_no = 1
        count = 1
            
        while True:

            params = {
                "query": "*",
                "sort": "Relevancy:asc",
                "page": page_no,
                "marketId": "NATIONAL",
                "showPermutedSearchParams": "false",
                "filter": f"pwCategoryPathIDs:{category_name}",
                "hitsPerPage": 32
            }

            response = requests.get(
                api_url,
                headers=HEADERS,
                params=params,
                impersonate="chrome"
            )

            if response.status_code == 200:

                data = response.json()

                hits = data.get("hits", [])

                if page_no == 3 or count == 34:
                    break

                for hit in hits:
                    slug = hit.get("masterValues", {}).get("slug", "")
                    if slug:
                        pdp_url = f"https://www.spar.at/produktwelt/{slug}"
                        response = requests.get(url=pdp_url, headers=HEADERS, impersonate="chrome")
                        
                        if response.status_code == 200:
                            self.parse_item(response, pdp_url)
                            count += 1
                        else:
                            logging.warning(f"Status code : {response.status_code}")

                page_no +=  1
                
            else:
                print(f"Status code : {response.status_code}")
                break
            

    def parse_item(self, response, url):
        
        sel = Selector(response.text)
        
        PRODUCT_NAME_XPATH = '//h1//text()'
        IMAGE_XPATH = '//div[@class="adaptive-image"]/img/@src'
        BREADCRUMB_XPATH = '//a[@class="link breadcrumbs__label"]/div/text()'
        DESCRIPTION_XPATH = '//div[@class="accordion-item__content"]/text()'
        SELLING_PRICE_XPATH = '//span[@class="product-price__price"]/text()'
        REGULAR_PRICE_XPATH = '//span[@class="product-price__price-old"]/text()'
        
        
        product_name = sel.xpath(PRODUCT_NAME_XPATH).getall()
        image = sel.xpath(IMAGE_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        product_description = sel.xpath(DESCRIPTION_XPATH).get()
        selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
        regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
        
        product_name = " ".join(product_name)
        breadcrumb = " > ".join(breadcrumb)
        selling_price = float(selling_price.replace(",", ".")) if selling_price else 0
        selling_price = f"{selling_price:.2f}" if selling_price != 0 else ""
        product_description = (
            product_description.replace("\n", "").replace("\t", " " )
            if product_description else ""
        )
        product_id = url.split("-")[-1].replace("p", "")
        regular_price = (
            regular_price.replace(",", ".")
            if regular_price else ""
        )
        regular_price = re.sub(r"[^\d.]", "", regular_price) 
        regular_price = f"{float(regular_price):.2f}" if regular_price else ""  
        
        item = {}
        
        item["product_name"] = product_name
        item["breadcrumb"] = breadcrumb
        item["selling_price"] = selling_price
        item["product_description"] = product_description
        item["image"] =  image
        item["article_number"] = product_id
        item["regular_price"] = regular_price
        item["product_id"] = product_id
        item["pdp_url"] = url
        
        logging.info(item)
        
        self.items.append(item)
        
    
    def to_csv(self):
       
       today = date.today().strftime("%Y_%m_%d")

       file_name = f"spar_{today}.csv"

       keys = self.items[0].keys()
       with open(file_name, "w", newline="", encoding="utf-8") as f:
           writer = csv.DictWriter(f, fieldnames=keys)
           writer.writeheader()
           writer.writerows(self.items)


                
if __name__ == "__main__":
    scrap = Scrape_data()
    scrap.start()
    
