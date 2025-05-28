import requests
from time import sleep
from settings import BASE_URL, HEADERS, USER_AGENTS, MONGO_URI, DB_NAME, CRAWLER_COLLECTION
from pymongo import MongoClient
import random
import logging


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]

    def start(self):
        product_page_base = "https://www.dm.si"
        page_size = 30
        current_page = 1
       

        while True:
            params = {
                "query": "vegansko",
                "allCategories.id": "040000",
                "pageSize": page_size,
                "searchType": "editorial-search",
                "sort": "editorial_relevance",
                "type": "search-static",
                "currentPage": current_page
            }

            HEADERS["user-agent"] = random.choice(USER_AGENTS)
            try:
                response = requests.get(BASE_URL, headers=HEADERS, params=params)
                if response.status_code == 200:
                    data = response.json()
                    products = data.get("products", [])

                    if  products:
                        for product in products:
                            relative_url = product.get("relativeProductUrl")
                            if relative_url:
                                full_url = f"{product_page_base}{relative_url}"

                                logging.info(full_url)
                                self.collection.insert_one({"url": full_url})  
                            
                        current_page += 1 
                        sleep(random.uniform(1, 3))
                    else:
                        logging.info("Completed successfully")
                        break
             
                elif response.status_code == 429:
                    sleep(random.uniform(10, 20))
                    continue 
        
                else:
                    logging.error(f"Status code: {response.status_code}")
                    break

            except Exception as e:
                logging.error("An error occurred:", e)


crawler = Crawler()
crawler.start()
