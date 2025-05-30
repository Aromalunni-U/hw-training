import requests
from parsel import Selector
import json

url = "https://www.next.co.uk/shop/gender-men-productaffiliation-clothing-0?p=1#0"

headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
}

################# CRAWLER ###########################

response = requests.get(url,headers=headers)
sel = Selector(response.text)
pdp_url = sel.xpath('//a[contains(@class, "MuiCardMedia-root")]/@href').getall()

################# PARSER ############################

url = "https://www.next.co.uk/style/st260486/c04288#c04288"

response = requests.get(url=url,headers=headers)

sel = Selector(response.text)


json_ld = sel.xpath(
    '//script[@type="application/ld+json" and @data-testid="pdp-structured-data"]/text()').get()

data = json.loads(json_ld)
offers = data.get("offers", [])

product_name_xpath = "//h1[@data-testid='product-title']/text()"
unique_id_xpath = "//span[@data-testid='product-code']/text()"
price_xpath = "//div[@data-testid='product-now-price']/span/text()"
review_xpath = "//span[@data-testid='rating-style-badge']/text()"
images_xpath = "//img[@class='percy-hide']/@src"
fit_type_xpath = '//div[@data-testid="fit-chips-button-group"]//button/text()'
rating_xpath = '//div[@class="MuiBox-root pdp-css-n0l63q"]/h3/text()'
composition_xpath = '//p[@data-testid="item-description-composition"]/text()'
description_xpath = '//p[@data-testid="item-description"]/text()'

product_name = sel.xpath(product_name_xpath).get()
unique_id = sel.xpath(unique_id_xpath).get()
price = sel.xpath(price_xpath).get()
review = sel.xpath(review_xpath).getall()
fit_types = sel.xpath(fit_type_xpath).getall()
images = sel.xpath(images_xpath).getall()
rating = sel.xpath(rating_xpath).get()
composition = sel.xpath(composition_xpath).get()
description = sel.xpath(description_xpath).get()

color = data.get("name").split(" Regular")[0] 
sizes = [offer["name"] for offer in offers if "name" in offer]
rating = data.get("aggregateRating",{}).get("ratingValue","")


###### Findings #########

# No pagination found, by changing the number in the URL, new product links are generated