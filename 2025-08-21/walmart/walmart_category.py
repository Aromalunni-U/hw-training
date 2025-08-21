import requests 
import logging
from parsel import Selector
from settings import  MONGO_URI, DB_NAME, HEADERS
from mongoengine import connect
from walmart_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")

    def start(self):
        url = "https://www.walmart.com/all-departments"
        
        response = requests.get(url = url, headers=HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)
            
            CATEGORY_XPATH = '//li[@class="pv1 pv0-m"]/a[contains(@href, "/cp/") or contains(@href,"/browse/")]/@href'
            
            urls = sel.xpath(CATEGORY_XPATH).getall()
            
            urls = [
                url if "https" in url  else f"https://www.walmart.com{url}" 
                for url in urls
            ]
            
            for url in urls:
                response = requests.get(url=url, headers=HEADERS)
                if response.status_code == 200:
                    self.sub_category_check(response, url)
                else:
                    logging.error(f"Status code : {response.status_code}")
                    
                        
    def sub_category_check(self , response, url):
        
        sel = Selector(response.text)
        data = sel.xpath('//h2[contains(text(), "Shop by")]/text()').get()
        if data:
            category_urls = sel.xpath(
                '//section[header/h2[contains(text(), "Shop by")]]//div[@role="listitem"]/a/@href'
            ).getall()
            
            for cat_url in category_urls:
                self.save_url(cat_url)
            
        else:
            
            url_data = sel.xpath(
                '//a[contains(@link-identifier,"Shop All") or contains(@link-identifier,"Shop all")]/@href'
                '| //a[contains(@link-identifier,"View all") or contains(@link-identifier,"View All")]/@href'
            ).get()

            if url_data:
                self.save_url(url_data)
            else:
                self.save_url(url)
                
    
    def save_url(self,link):
        try:
            logging.info(link)
            CategoryItem(url = link).save()
        except:
            pass 


if __name__ == "__main__":
    category = Category()
    category.start()