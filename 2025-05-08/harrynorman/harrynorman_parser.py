import  json
import re
import logging
import cloudscraper
from parsel import Selector
from harrynorman_crawler import crawler
from settings import BASE_URL, JSON_PATH


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"
)

scraper = cloudscraper.create_scraper()

def parser(agent_urls):
    try:
        for url in agent_urls:
            response = scraper.get(url)
            if response.status_code == 200:
                selector = Selector(response.text)

                name_xpath = "//section[@class='rng-bio-account-content-office']/h1/text()"
                communities_xpath = '//section[@class="rng-bio-account-content-office"]//span[small[text()="Communities"]]/text()'
                market_areas_xpath = '//section[@class="rng-bio-account-content-office"]//span[small[text()="Market Areas"]]/text()'
                agent_website_xpath = '//a[text()="Visit my site"]/@href'
                agent_image_xpath = '//div[@class="site-account-image"]/@style'
                mobile_phone_xpath = '//li/strong[text()="Mobile Phone"]/following-sibling::a/text()'

                agent_name = selector.xpath(name_xpath).get()
                communities = selector.xpath(communities_xpath).get()
                market_areas =selector.xpath(market_areas_xpath).get()
                agent_website = selector.xpath(agent_website_xpath).get()
                agent_image = selector.xpath(agent_image_xpath).get()
                mobile_phone = selector.xpath(mobile_phone_xpath).get()

                communities = communities if communities else "Not Available"
                market_areas = market_areas if market_areas else "Not Available"
                agent_website = agent_website if agent_website else "Not Available"
                agent_image = re.search(r'url\((https?://[^\)]+)\)', agent_image).group(1)
                mobile_phone = mobile_phone if mobile_phone else "Not Available"

                yield {
                    "agent_url":url,
                    "agent_name":agent_name,
                    "agent_image":agent_image,
                    "agent_phone":mobile_phone,
                    "agent_website":agent_website,
                    "communities":communities,
                    "market_areas":market_areas
                }

            else:
                logging.error("status code: ", response.status_code)
    except Exception as e:  
        logging.error(f"An error occured: {e}")



agent_links = crawler(BASE_URL)
data = list(parser(agent_links))

with open(JSON_PATH, "w") as file:
    json.dump(data, file, indent=4)


logging.info("Completed Succssfully")
