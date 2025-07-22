import cloudscraper
from parsel import Selector
from pymongo import MongoClient
import json
import logging
from settings import   (
    HEADERS, MONGO_URI,DB_NAME,headers, DATA_COLLECTION
)   


scraper = cloudscraper.create_scraper()

url = "https://www.homerealestate.com/CMS/CmsRoster/RosterSearchResults"


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.collection = self.client[DB_NAME][DATA_COLLECTION]
    
    def start(self):
        for number in range(1,21):
                    
                params = {
                    "layoutID": "956",
                    "pageSize": "10",
                    "pageNumber": str(number),
                    "sortBy": "random"
                }

                response = scraper.get(url, headers=HEADERS, params=params)

                if response.status_code == 200:
                     self.parse_item(response)

    
    def parse_item(self,response):
             
        data = response.json() 
        data = json.loads(data) 

        html_data = data.get("Html", "")
        sel = Selector(text=html_data)


        articles = sel.xpath("//article[contains(@class,'rng-agent-roster-agent-card')]")

        for article in articles:

            profile_url = article.xpath(".//a[contains(@href,'bio')]/@href").get()
            name = article.xpath(".//h1[@class='rn-agent-roster-name js-sort-name']/text()").get()
            image_url = article.xpath(".//img/@src").get()
            office_phone_numbers  = article.xpath(".//a[i[contains(@class, 'rni-company')]]/@href").get()
            agent_phone_numbers = article.xpath(".//a[i[contains(@class,'rni-profile')]]/@href").get()
            city = article.xpath(".//span[@class='js-sort-city']/text()").get()
            email = article.xpath(".//a[i[contains(@class,'rni-mail')]]/@href").get()
            website = article.xpath(".//a[i[contains(@class,'rni-website')]]/@href").get()
            full_address = article.xpath(".//p[span[@class='js-sort-city']]//text()[normalize-space()]").getall()
            title = article.xpath(".//span[@class='account-title']/text()").get()

            profile_url = f"https://www.homerealestate.com{profile_url}" if profile_url else ""
            name = name.strip() if name else ""

            address = ", ".join([part.replace("|","").strip() for part in full_address[1:-1] if part.strip()])

            state_zip = full_address[-2].strip('| ')
            state, zipcode = state_zip.split()
            
            city = city.strip() if city else ""
            agent_phone_numbers = agent_phone_numbers.replace("tel:","") if agent_phone_numbers else ""
            office_phone_numbers = office_phone_numbers.replace("tel:","") if office_phone_numbers else ""
            title = title.strip() if title else ""

            social = ""
            description = ""

            if profile_url:
                response = scraper.get(profile_url, headers=headers)
                sel = Selector(response.text)

                FACEBOOK_XPATH = '//a[@aria-label="Facebook"]/@href'
                INSTAGRAM_XPATH = '//a[@aria-label="Instagram"]/@href'
                DESCRIPTION_XPATH = '//div[@id="bioAccountContentDesc"]//p/text()'

                facebook = sel.xpath(FACEBOOK_XPATH).get()
                instagram = sel.xpath(INSTAGRAM_XPATH).get()
                description = sel.xpath(DESCRIPTION_XPATH).getall()
                description = " ".join(description) if description else ""

                social = {}
                social["facebook"] = facebook
                social["instagram"] = instagram


            item = {}

            item["name"] = name
            item["title"] = title
            item["city"] = city  
            item["zipcode"] = zipcode
            item["state"] = state
            item["address"] = address
            item["profile_url"] = profile_url  
            item["description"] = description  
            item["website"] = website  
            item["email"] = email  
            item["image_url"] = image_url  
            item["agent_phone_numbers"] = agent_phone_numbers  
            item["office_phone_numbers"] = office_phone_numbers  
            item["social"] = social  

            logging.info(item)
            self.collection.insert_one(item)


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
