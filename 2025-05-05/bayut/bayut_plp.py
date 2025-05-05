import requests
from parsel import Selector
from urllib.parse import urljoin
from settings import HEADERS


def get_product_links(url):
    product_links = []  
    page_count = 1
    
    while url and page_count <= 10:
        response = requests.get(url,headers=HEADERS)
        if response.status_code == 200:
            selector = Selector(response.text)

            links = selector.xpath("//div[@class='dde89f38']/a[@class='d40f2294']/@href").getall()
            product_links.extend(links) 

            print(f"Found {len(links)} product links on page {page_count}")
            
            next_page = selector.xpath("//a[@title='Next']/@href").get()
            if next_page:
                url = urljoin(url, next_page) 
            else:
                url = None 
            page_count += 1

        else:
            print(f"Failed to retrieve page: {response.status_code}")
            break
    
    return product_links