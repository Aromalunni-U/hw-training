import re
import json
import logging
from settings import *
from urllib.parse import urljoin
from parsel import Selector
from playwright.sync_api import sync_playwright

def Crawler():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(BASE_URL)
            page.wait_for_selector(".site-roster-card-image-link")
            page.wait_for_timeout(3000)

            html = page.content()
            sel = Selector(text=html)

            agent_links_raw = sel.xpath("//a[@class='site-roster-card-image-link']/@href").getall()
            agent_names = sel.xpath("//div[@class='site-roster-card-content']/h2/text()").getall()
            phones = sel.xpath("//li/a[contains(@href,'tel:')]/text()").getall()
            raw_image_urls = sel.xpath("//div[@class='site-roster-card-image']/@style").getall()

            agent_links = [urljoin(BASE_URL, link) for link in agent_links_raw]
            image_urls = [re.search(r'url\((.*?)\)', style).group(1) for style in raw_image_urls]

            agents = []
            for link, name, phone,  img in zip(agent_links, agent_names, phones,  image_urls):
                agents.append({
                    "agent_link": link,
                    "agent_name": name,
                    "phone": phone,
                    "image_url": img
                })
            return agents

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            browser.close()


data = Crawler()

with open(JSON_PATH,"w") as file:
    json.dump(data, file, indent=4)

logging.info("Completed successfully")