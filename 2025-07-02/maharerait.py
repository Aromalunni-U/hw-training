import requests
from parsel import Selector

HEADERS = {
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "upgrade-insecure-requests": "1",
}


url = "https://maharera.maharashtra.gov.in/projects-search-result"
res = requests.get(url=url, headers=HEADERS)
sel = Selector(res.text)

form_build_id = sel.xpath('//input[@name="form_build_id"]/@value').get()
form_id = sel.xpath('//input[@name="form_id"]/@value').get()

payload = {
    "project_name": "",
    "project_location": "",
    "project_completion_date": "",
    "project_state": "27",         #Maharashtra
    "project_division": "5",       #Pune
    "project_district": "",        
    "form_build_id": form_build_id,
    "form_id": form_id,
    "op": "Search"
}

response = requests.post(url, data=payload, headers=HEADERS)
sel = Selector(response.text)

REGISTRATION_ID_XPATH = './/div[@class="col-xl-4"]/p[1]/text()'
PROJECT_NAME_XPATH = './/div[@class="col-xl-4"]/h4/strong/text()'
PROMOTER_NAME_XPATH = './/div[@class="col-xl-4"]/p[@class="darkBlue bold "]/text()'
LOCATION_XPATH = './/ul[@class="listingList"]/li[1]/a/text()'
STATE_XPATH = './/div[contains(text(), "State")]/following-sibling::p/text()'
PINCODE_XPATH = './/div[contains(text(), "Pincode")]/following-sibling::p/text()'
DISTRICT_XPATH = './/div[contains(text(), "District")]/following-sibling::p/text()'
LAST_MODIFIED_XPATH = './/div[contains(text(), "Last Modified")]/following-sibling::p/text()'
PROJECT_LINK_XPATH = './/a[contains(text(), "View Details")]/@href'

cards = sel.xpath('//div[contains(@class, "row shadow p-3 mb-5 bg-body rounded")]')

for card in cards:
        registration_id =  card.xpath(REGISTRATION_ID_XPATH).get()
        project_name =  card.xpath(PROJECT_NAME_XPATH).get()
        promoter_name =  card.xpath(PROMOTER_NAME_XPATH).get()
        location =  card.xpath(LOCATION_XPATH).get()
        state =  card.xpath(STATE_XPATH).get()
        pincode =  card.xpath(PINCODE_XPATH).get()
        district =  card.xpath(DISTRICT_XPATH).get()
        last_modified =  card.xpath(LAST_MODIFIED_XPATH).get()
        project_link =  card.xpath(PROJECT_LINK_XPATH).get()

