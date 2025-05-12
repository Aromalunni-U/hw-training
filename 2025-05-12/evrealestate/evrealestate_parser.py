import requests
import logging
from parsel import Selector
from settings import BASE_URL
from tqdm import tqdm
from pymongo import MongoClient
from settings import MONGO_URI, DB_NAME, PARSE_COLLECTION, CRAWLER_COLLECTION, BASE_URL
from evrealestate_crawler import crawler



client = MongoClient(MONGO_URI)  
db = client[DB_NAME] 
crawler_collection = db[CRAWLER_COLLECTION] 
parser_collection = db[PARSE_COLLECTION]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"
)

def parser(agent_urls):
    for url in tqdm(agent_urls):
        response = requests.get(url)
        if response.status_code == 200:
            selector = Selector(response.text)

            name_xpath = '//h1[@data-testid="advisor-name"]/text()'
            language_xpath = '//span[@data-testid="language-values"]/text()'
            img_xpath = '//div[@class="sc-d4994099-2 fZYlOn"]/img/@src'
            phone_xpath = '//div[@data-testid="advisor-phone"]/a/text()'
            shop_xpath  = '//a[@data-testid="advisor-office-name"]/text()'
            shop_link_xpath = '//a[@data-testid="advisor-office-name"]/@href'
            website_xpath = '//a[@data-testid="advisor-website-personal"]/@href'
            address_xpath = '//div[@data-testid="advisor-office-address"]/text()'
            postal_code_xpath = '//div[@data-testid="advisor-office-cityzipcode"]/text()'

            name = selector.xpath(name_xpath).get()
            language = selector.xpath(language_xpath).get()
            img_link = selector.xpath(img_xpath).get()
            phone = selector.xpath(phone_xpath).get()
            shop = selector.xpath(shop_xpath).get()
            shop_link = selector.xpath(shop_link_xpath).get()
            website = selector.xpath(website_xpath).get()
            address = selector.xpath(address_xpath).get()
            state = selector.xpath(postal_code_xpath).get()
            city = selector.xpath(postal_code_xpath).get()
            postal_code = selector.xpath(postal_code_xpath).get()

            language = language if language else "Not available"
            phone = phone if phone else "Not available"
            website = website if website else "Not available"
            address = address.strip() if address else "Not available"
            state = state.split()[1].strip() if state else "Not available"
            city = city.split(",")[0].strip() if city else "Not available"
            postal_code = postal_code.split()[-1].strip()  if postal_code else "Not available"
            email = ".".join(name.lower().split()) + "@evrealestate.com"

            yield {
                "agent_url": url,
                "name": name,
                "img_link": img_link,
                "language": language,
                "phone": phone,
                "email": email,
                "shop": shop,
                "shop_link": shop_link,
                "website": website,
                "state": state,
                "city": city,
                "postal_code": postal_code,
                "address": address,
            }
        
        else:
            logging.error(f"An error occured {url}: {response.status_code}")
            continue



agent_links = crawler(BASE_URL)

if agent_links:
    crawler_collection.insert_many([{"agent_url": link} for link in agent_links])

data = list(parser(agent_links))

if data:
    parser_collection.insert_many(data)
    logging.info("Data inserted into MongoDB successfully.")

