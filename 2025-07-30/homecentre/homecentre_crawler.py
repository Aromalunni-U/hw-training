import requests
import logging
from pymongo import MongoClient
from settings import headers, DB_NAME, MONGO_URI, CRAWLER_COLLECTION



class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.collection = self.client[DB_NAME][CRAWLER_COLLECTION]
    
    def start(self):
        url = "https://3hwowx4270-1.algolianet.com/1/indexes/*/queries"

        for page_no in range(5): 
            payload = {
                "requests": [
                    {
                        "indexName": "prod_uae_homecentre_Product",
                        "params": f"query=*&hitsPerPage=42&page={page_no}&facets=*&facetFilters=[\"inStock:1\",\"approvalStatus:1\",\"allCategories:furniture-sofaandseating\",\"badge.title.en:-LASTCHANCE\"]&attributesToRetrieve=url,name"
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print(response)

                data = response.json()
                products = data["results"][0]["hits"]
                for product in products:
                    url_data = product.get("url", {})
                    for category, lang_map in url_data.items():
                        pdp_url = lang_map.get("en", "")
                        if pdp_url:
                            pdp_url = f"https://www.homecentre.com/ae/en{pdp_url}"
                            logging.info(pdp_url)
                            self.collection.insert_one({"url": pdp_url})

            else:
                logging.error(f"Status code : {response.status_code}")




if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()