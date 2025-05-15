from playwright.sync_api import sync_playwright
from time import sleep
from parsel import Selector
from urllib.parse import urljoin
from settings import *


def Crawler(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto(url)

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
        estate_links = [urljoin(url,l) for l in links]

        logging.info(f"Total links: {len(estate_links)}")
        browser.close()

        return estate_links
        


