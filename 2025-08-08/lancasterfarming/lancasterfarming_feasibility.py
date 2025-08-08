import requests
from parsel import Selector


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

########################## CRAWLER ###################

url = "https://www.lancasterfarming.com/classifieds/farm_equipment/?l=15"

while True:

    response = requests.get(url=url, headers=HEADERS)
    if response.status_code == 200:
        sel = Selector(response.text)
        links = sel.xpath(
            '//div[@id="classifieds-results-container"]//div[@class="image"]/a/@href').getall()
        
        links = [f"https://www.lancasterfarming.com{link}" for link in links]
        for link in links:
            print(link)
            c+=1

        next_page = sel.xpath('//li[@class="next"]/a/@href').get()
        if not next_page:
            break
        url = f"https://www.lancasterfarming.com{next_page}"
    else:
        print(f"Status code :{response.status_code}")
    

########################## PARSER ####################

url = "https://www.lancasterfarming.com/classifieds/farm_equipment/2--used-grain-legs/pdfdisplayad_6b825a32-101c-53c1-a61f-88393b2ebb60.html"

response = requests.get(url=url, headers=HEADERS)
if response.status_code == 200:
    sel = Selector(response.text)

    TITLE_XPATH = '//h1[@class="title"]/text()'
    IMAGE_XPATH = '//div[@class="hover-expand"]/a/img/@src'
    CATEGORY_XPATH = '//div[contains(@class, "category")]/ul[@class="list-inline"]/li/a/text()'
    DETAILS_XPATH = '//div[@class="panel-body"]/pre/text()'

    title = sel.xpath(TITLE_XPATH).get()
    image = sel.xpath(IMAGE_XPATH).get()
    category = sel.xpath(CATEGORY_XPATH).get()
    details = sel.xpath(DETAILS_XPATH).get()


else:
    print(f"Status code :{response.status_code}")
    

