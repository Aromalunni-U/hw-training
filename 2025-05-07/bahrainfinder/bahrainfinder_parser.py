import json
import logging
import requests
from tqdm import tqdm
from parsel import Selector
from urllib.parse import urljoin
from bahrainfinder_crawler import crawler
from settings import HEADERS, BASE_URL, JSON_PATH


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"
)

def parser(property_links, url):
    try:
        for link in tqdm(property_links):
            property_url = urljoin(url,link)
            response = requests.get(property_url, headers=HEADERS)  
            if response.status_code == 200:
                selector = Selector(response.text)

                bf_id_xpath = "//li[@id='bf-id']/strong/text()"
                title_xpath = "//div[@class='page-title']/h1/text()"
                currency_xpath = "//ul[@class='price-wrap-hide-on']/span/text()"
                price_xpath = "//ul[@class='price-wrap-hide-on']/span/strong/text()"
                property_size_xpath = "//i[contains(@class,'icon-real-estate-dimensions-plan')]/following-sibling::strong/text()"
                property_usage_xpath = "//li[@id='usage']/strong/text()"
                batn_xpath = "//i[contains(@class, 'icon-bathroom-shower')]/following-sibling::strong/text()"
                beadroom_xpath = "//i[contains(@class, 'icon-hotel-double-bed')]/following-sibling::strong/text()"
                halls_xpath = "//i[contains(@class, 'real-estate-dimensions-block')]/following-sibling::strong/text()"
                furnish_xpath = "//li[@id='furnished']/strong/text()" 
                garage_xpath = "//i[contains(@class, 'icon-car')]/following-sibling::strong/text()"
                agent_xpath = "//p[@class='agent-name']/text()"
                agent_no_xpath = "//a[@title='Call']/span[@class='show-on-click']/text()"
                features_xpath = "//i[contains(@class,'fas')]/following-sibling::a/text()"
                images_xpath = "//a[@class='spotlight']/img/@src"

                bf_id = selector.xpath(bf_id_xpath).get()
                title = selector.xpath(title_xpath).get()
                currency = selector.xpath(currency_xpath).get()
                price = selector.xpath(price_xpath).get()
                property_size = selector.xpath(property_size_xpath).get()
                property_usage = selector.xpath(property_usage_xpath).get()
                bathroom = selector.xpath(batn_xpath).get()
                beadroom = selector.xpath(beadroom_xpath).get()
                halls = selector.xpath(halls_xpath).get()
                furnsih = selector.xpath(furnish_xpath).get()
                garage = selector.xpath(garage_xpath).get()
                agent = selector.xpath(agent_xpath).get()
                agent_no = selector.xpath(agent_no_xpath).get()
                features = selector.xpath(features_xpath).getall()
                images = selector.xpath(images_xpath).getall()

                currency = currency.replace(".","").strip()
                property_size = property_size.replace("\u00b2","2").strip()
                bathroom = bathroom.strip() if bathroom else "Not Available"
                beadroom = beadroom.strip() if beadroom else "Not Available"
                features = features if features else "Not Available"
                halls = halls if halls else "Not Available"
                furnsih = furnsih if furnsih else "Not Available"
                garage = garage if garage else "Not Available"

                yield {
                    "url": property_url,
                    "bf_id": bf_id,
                    "property_title": title,
                    "currency": currency,
                    "price": price,
                    "property_size": property_size,
                    "property_usage": property_usage,
                    "bedroom": beadroom,
                    "bathroom": bathroom,
                    "halls":halls,
                    "furnish":furnsih,
                    "garage":garage,
                    "agent":agent,
                    "agent_no":agent_no,
                    "features": features,
                    "images": images
                }

            else:
                logging.error("status code: ", response.status_code)
    except Exception as e:  
        logging.error(f"An error occured: {e}")



links = crawler(BASE_URL)
data = list(parser(links,BASE_URL))

with open(JSON_PATH,"w") as file:
    json.dump(data, file, indent=4)

logging.info("Completed Succssfully")
