import requests
from parsel import Selector


headers = {
    "accept-encoding":"gzip, deflate",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

###################### CRAWLER #########################

url = "https://www.lego.com/en-in/categories/all-sets"

response = requests.get(url,headers=headers)

print(response.text)
response = Selector(response.text)

products_urls = response.xpath(
    '//div[@data-test="product-leaf-action-row"]/a/@href'
    ).getall()

print(products_urls)

###################### PARSER ###########################


url = "https://www.lego.com/api/graphql/ProductDetails"

params = {
    "variables": '{"slug":"venator-class-republic-attack-cruiser-75367"}',
    "extensions": '{"locale":"en-IN","persistedQuery":{"version":1,"sha256Hash":"40fed00a62a3fc6939e86f25af6bf7604a81992012f22cd079e1341854deee22"}}'
}

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "x-apollo-operation-name": "ProductDetails",
    "referer": "https://www.lego.com/en-in/product/venator-class-republic-attack-cruiser-75367",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "x-locale": "en-IN"
}

response = requests.get(url, headers=headers, params=params)

data = response.json()

data = data.get("data",{}).get("product",{})
attributes = data.get("readOnlyVariant",{}).get("attributes",{})
product_media = data.get("productMedia", {}).get("items", [])


product_code = data.get("productCode","")
product_name = data.get("name","")
ages = attributes.get("ageRange","")
piece_count = attributes.get("pieceCount","")
build_height = attributes.get("buildHeight","")
build_width = attributes.get("buildWidth","")
build_depth = attributes.get("buildDepth","")
minifigure_count = attributes.get("minifigureCount","")
description = data.get("description","")
features = data.get("featuresText","")
images = [
    img["baseImgUrl"] for img in product_media if img.get("__typename") == "ProductImage"
]

########### FINDING ##################

# Unique set number or product code  found at the end of each URL