import re
import logging
import cloudscraper
from urllib.parse import urljoin
from settings import HEADERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"
)

scraper = cloudscraper.create_scraper()
scraper.headers.update(HEADERS)

agent_links = []

def crawler(url_template):
    page_number = 1
    while True:
        url = url_template.format(page_number=page_number)
        logging.info(f"Scraping page {page_number} ...")

        try:
            response = scraper.get(url)
            if response.status_code == 200:

                pattern = r'/bio/[^\\"]+'
                matches = re.findall(pattern, response.text)

                if matches:
                    full_urls = [urljoin(url, match) for match in matches]
                    agent_links.extend(full_urls)
                else:
                    break
                page_number += 1 

            else:
                logging.warning(f"Status code {response.status_code}")
        except Exception as e:
            logging.error(f"Error occurred while scraping page {page_number}: {e}")

    logging.info(f"Total agent URLS collected: {len(agent_links)}")
    return agent_links
