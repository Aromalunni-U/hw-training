import re
import logging
import cloudscraper
from parsel import Selector
from tqdm import tqdm
from pymongo import MongoClient
from harrynorman_crawler import crawler
from settings import BASE_URL, MONGO_URI, DB_NAME, COLLECTION_NAME


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"
)

scraper = cloudscraper.create_scraper()

def parser(agent_urls):
    try:
        for url in tqdm(agent_urls):
            response = scraper.get(url)
            if response.status_code == 200:
                selector = Selector(response.text)

                name_xpath = "//section[@class='rng-bio-account-content-office']/h1/text()"
                agent_image_xpath = '//div[@class="site-account-image"]/@style'
                mobile_phone_xpath = '//li/strong[text()="Mobile Phone"]/following-sibling::a/text()'
                agent_website_xpath = '//a[text()="Visit my site"]/@href'
                office_name_xpath = '//section[@class="rng-bio-account-content-office"]/div[1]/strong/text()'
                communities_xpath = '//section[@class="rng-bio-account-content-office"]//span[small[text()="Communities"]]/text()'
                market_areas_xpath = '//section[@class="rng-bio-account-content-office"]//span[small[text()="Market Areas"]]/text()'
                contact_url_xpath = '//a[text()="Contact Me"]/@href'

                agent_name = selector.xpath(name_xpath).get()
                agent_image_raw = selector.xpath(agent_image_xpath).get() 
                mobile_phone = selector.xpath(mobile_phone_xpath).get()
                agent_website = selector.xpath(agent_website_xpath).get()
                office_name_raw = selector.xpath(office_name_xpath).get()
                communities = selector.xpath(communities_xpath).get()
                market_areas =selector.xpath(market_areas_xpath).get()
                contact_url = selector.xpath(contact_url_xpath).get()

                communities = communities if communities else "Not Available"
                market_areas = market_areas if market_areas else "Not Available"
                agent_website = agent_website if agent_website else "Not Available"
                office_name = office_name_raw.split('|')[-1].strip() if office_name_raw else "Not Available"
                if agent_image_raw:
                    match = re.search(r'url\((https://[^\)]+)\)', agent_image_raw)
                    if match:
                        agent_image = match.group(1)
                mobile_phone = mobile_phone if mobile_phone else "Not Available"
                contact_url = contact_url if contact_url else "Not Available"

                yield {
                    "agent_url":url,
                    "agent_name":agent_name,
                    "agent_image":agent_image,
                    "agent_phone":mobile_phone,
                    "agent_website":agent_website,
                    "office_name":office_name,
                    "communities":communities,
                    "market_areas":market_areas,
                    "contact_url":contact_url
                }

            else:
                logging.error(f"Status code: {response.status_code}")
    except Exception as e:  
        logging.error(f"An error occured: {e}")


agent_links = crawler(BASE_URL)
data = list(parser(agent_links))

client = MongoClient(MONGO_URI)  
db = client[DB_NAME] 
collection = db[COLLECTION_NAME] 

if data:
    collection.insert_many(data)
    logging.info("Data inserted into MongoDB successfully.")

