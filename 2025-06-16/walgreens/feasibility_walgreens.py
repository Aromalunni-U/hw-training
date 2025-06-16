import re
import requests
from parsel import Selector
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www.walgreens.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
}


############## CRAWLER ############################

url = "https://www.walgreens.com/sitemap-pdp.xml"

response = requests.get(url=url,headers=headers)
pdp_urls = re.findall(r'<loc>(.*?)</loc>',response.text)

################ PARSER ############################

pdp_url = "https://www.walgreens.com/store/c/nivea-men-maximum-hydration-face-lotion-with-broad-spectrum-spf-15-sunscreen-for-men/ID=prod1296860-product"

product_id = pdp_url.split("ID=")[1].split("-product")[0]

api_url = "https://www.walgreens.com/productapi/v1/products"

params = {
    "productId": product_id,
    "storeId": "15196",
    "deliveredCity": "Chicago",
    "deliveredState": "IL"
}

response = requests.get(api_url, params=params,headers=headers)
data = response.json()

product_info = data.get("productInfo",{})
price_info = data.get("priceInfo",{})
section = data.get("prodDetails",{}).get("section",[])

product_name = product_info.get("title","")
category = product_info.get("productType","")
brand = product_info.get("brandName","")
image_urls = product_info.get("filmStripUrl",[])
grammage = product_info.get("sizeCount","")
breadcrumb = " > ".join([
    "Home",
    "Shop",
    product_info.get("tier1Category", ""),
    product_info.get("tier2Category", ""),
    product_info.get("tier3Category", "")
])
images = [
    img for img in image_urls 
    for k,v in img.items()
    if "zoomImageUrl" in k 
    ]
upc = data.get("inventory",{}).get("upc","")
regular_price = price_info.get("regularPrice","")
price_per_unit = price_info.get("unitPrice","")
promotion_description = price_info.get("rebateOffers").get("rebateText","")
product_description = section[0].get("description",{}).get("productDesc","")
ingredients = section[1].get("ingredients",{}).get("ingredientGroups",[])[0].get("ingredientTypes")[0].get("ingredients")
warning = section[2].get("warnings",{}).get("productWarning","")
review = section[5].get("reviews",{}).get("reviewCount","")
rating = section[5].get("reviews").get("overallRating","")

parts = grammage.split(" ", 1)
grammage_quantity = parts[0]     
grammage_unit = parts[1]  


