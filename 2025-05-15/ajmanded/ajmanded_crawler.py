from playwright.sync_api import sync_playwright
from time import sleep
import logging
from parsel import Selector
from urllib.parse import urljoin
from settings import *
from pymongo import MongoClient


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]

    def start(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=False, slow_mo=100)
            page = self.browser.new_page()
            page.goto(BASE_URL)

            page.wait_for_selector(".selectize-control")
            page.click(".selectize-control")
            page.click("div[data-value='N']")

            page.wait_for_selector("#LicenseTradeName", state="visible")
            page.fill("#LicenseTradeName", "real estate")

            input("Press ENTER")

            page.click("button[type='submit']")
            page.wait_for_selector(".result")
            
            sleep(5)

            sel = Selector(page.content())
            links_xpath = "//a[contains(@class, 'btn-view')]/@href"
            links = sel.xpath(links_xpath).getall()
            estate_links = [urljoin(BASE_URL,l) for l in links]
            logging.info(f"Total links: {len(estate_links)}")

            data = [{"real_estate_link": link} for link in estate_links]
            self.collection.insert_many(data)
            logging.info("Completed successfully")

    def close(self):
        self.client.close()
        logging.info("Connection closed.")


crawler = Crawler()
crawler.start()
crawler.close()


