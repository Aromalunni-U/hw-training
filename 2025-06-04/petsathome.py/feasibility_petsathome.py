import requests
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from parsel import Selector


headers = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}


########################## CRAWLER ############################

search_url = "https://www.petsathome.com/search?searchTerm={}"

EAN = '76344107521'
response = requests.get(search_url.format(EAN),headers=headers)

sel = Selector(response.text)
pdp_url = sel.xpath('//a[@class="product-tile_wrapper__T0IlX"]/@href').get()
pdp_url = "https://www.petsathome.com" + pdp_url


############################# PARSER ###############################


pdp_url = "https://www.petsathome.com/product/wellness-core-complete-medium-breed-dry-adult-dog-food-turkey-with-chicken/7122687P?productId=7122687&purchaseType=easy-repeat&weight=1.8kg"

path_parts = urlparse(pdp_url).path.strip("/").split("/")

product_code = path_parts[-1]
slug = path_parts[-2]
product_id =  parse_qs(urlparse(pdp_url).query)["productId"][0]

json_url = f"https://www.petsathome.com/_next/data/YwW8A4A1S_S24O3mB04Mu/en/product/{slug}/{product_code}.json?productId={product_id}&slug={slug}&slug={product_code}"


response = requests.get(json_url,headers=headers)

data = response.json()
product_details = data.get("pageProps",{}).get("baseProduct",{})
product_list = product_details.get("products",[{}])
offers = product_details.get("offerTermsAndConditions", [])

brand = product_details.get("brand","")
images = product_details.get("imageUrls",[])
rating = data.get("pageProps",{}).get("productRating",{}).get("averageRating","")
review = data.get("pageProps",{}).get("productRating",{}).get("reviewCount","")
material_composition = product_details.get("composition","")
product_unique_key = product_details.get("baseProductId","")
product_name = product_details.get("name","")
product_description = product_details.get("description","")
netweight = product_list[0].get("label","")
price = product_list[0].get("price",{}).get("base","")
features = product_details.get("featuresAndBenefits",[])
promotion_description = offers[0].get("header","")
feeding_recommendation = product_details.get("guides",[{}])[0].get("introduction")
ingredients = product_details.get("additives",{}).get("analyticalConstituents","")

valid_upto = offers[0].get("body",[])[1]
match = re.search(
    r"(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4})",
    valid_upto
)
valid_upto =  re.sub("st|nd|rd|th", "", match.group())
dt = datetime.strptime(valid_upto, "%d %B %Y")
valid_upto = dt.strftime("%Y-%m-%d")

