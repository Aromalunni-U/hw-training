import requests
from parsel import Selector
from settings import HEADERS
from urllib.parse import urljoin


def crawler(url):
    property_links = []
    page_count = 1

    while url and page_count<11:
        response = requests.get(url,headers=HEADERS)
        if response.status_code == 200:
            selector = Selector(response.text)

            property_link_xpath = "//div[@class='listing-thumb']/a/@href"
            next_page_xpath = "//a[@aria-label='Next']/@href"

            links = selector.xpath(property_link_xpath).getall()
            property_links.extend(links)

            next_page = selector.xpath(next_page_xpath).get()

            if next_page:
                url = urljoin(url,next_page)
            else:
                url = None
            page_count += 1
        else:
            print("Status code:", response.status_code)
            break
    return property_links
    

