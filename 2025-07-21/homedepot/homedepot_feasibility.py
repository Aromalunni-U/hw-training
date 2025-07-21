import requests
from parsel import Selector
from settings import BASE_URL, HEADERS
import json

################ CRAWLER ################

category_url = "https://www.homedepot.com/b/Cleaning-Laundry-Supplies/N-5yc1vZcb4s?catStyle=ShowProducts"

page = 0

while True:
    url = f"{category_url}&Nao={page}"

    response = requests.get(url, headers= HEADERS)
    sel = Selector(response.text)

    pdp_links = sel.xpath('//div[@data-testid="product-pod"]/a/@href').getall()
    pdp_links = [f"https://www.homedepot.com{link}" for link in pdp_links]

    json_text = sel.xpath('//script[@id="thd-helmet__script--browseSearchStructuredData"]/text()').get()
    data = json.loads(json_text)

    for block in data:
        entity = block.get("mainEntity")
        if entity and "offers" in entity:
            offers = entity["offers"]
            products = offers.get("itemOffered", [])
            for item in products:
                offer = item.get("offers")
                if offer and "url" in offer:
                    pdp_links.append(offer["url"])

    if not pdp_links:
        break

    for url in pdp_links:
        print(url)    


    page += 24


############## PARSER ##################


url = "https://www.homedepot.com/p/JoyJolt-JoyFul-6-Piece-Kitchen-Storage-Jars-with-Airtight-Bamboo-Clamp-Lids-JW10504/319937634"

response = requests.get(url, headers= HEADERS)
sel = Selector(response.text)

breadcrumb = sel.xpath('//div[contains(@class,"breadcrumb__item")]/a/text()').getall()
retail_limit = sel.xpath('//div[contains(text(), "per order")]/text()').get()
json_ld_text = sel.xpath("//script[@id='thd-helmet__script--productStructureData']/text()").get()
details_script = sel.xpath('//script[contains(text(), "window.__APOLLO_STATE__")]/text()').get()

product_data = json.loads(json_ld_text)

product_name = product_data.get("name")
images = product_data.get("image", [])
brand = product_data.get("brand", {}).get("name")
aggregate_rating = product_data.get("aggregateRating", {})
rating = aggregate_rating.get("ratingValue", "")
review = aggregate_rating.get("reviewCount", "")
product_description = product_data.get("description", "")
currency = product_data.get("offers", {}).get("priceCurrency", "")
price_was = product_data.get("offers", {}).get("priceSpecification", {}).get("price", "")


# product details

start = details_script.find('{')
end = details_script.rfind('}') + 1
apollo_data = json.loads(details_script[start:end])

for key in apollo_data:
    if key.startswith("base-catalog-"):
        base_data = apollo_data[key]
        break

product_details = {}
groups = base_data.get("specificationGroup", [])
for group in groups:
    for spec in group.get("specifications", []):
        product_details[spec["specName"]] = spec["specValue"]

