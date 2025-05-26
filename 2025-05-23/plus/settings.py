import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://www.plus.nl/screenservices/ECP_Composition_CW/ProductLists/PLP_Content/DataActionGetProductListAndCategoryInfo"

HEADERS_CAT_1 = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Origin": "https://www.plus.nl",
    "Referer": "https://www.plus.nl/producten/frisdrank-sappen-koffie-thee/frisdrank",
    "x-csrftoken": "T6C+9iB49TLra4jEsMeSckDMNhQ=", 
}
HEADERS_CAT_2 = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Origin": "https://www.plus.nl",
    "Referer": "https://www.plus.nl/producten/zuivel-eieren-boter/verse-zuivel/melk-karnemelk",
    "x-csrftoken": "T6C+9iB49TLra4jEsMeSckDMNhQ=", 
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 Chrome/95.0.4638.74 Mobile Safari/537.36",
]

API_URL = "https://www.plus.nl/screenservices/ECP_Product_CW/ProductDetails/PDPContent/DataActionGetProductDetailsAndAgeInfo"

API_HEADERS = {
    "user-agent":"",
    "x-csrftoken":"T6C+9iB49TLra4jEsMeSckDMNhQ=",
    "referer":""
}


MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "plus"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  

file_name = "2025-05-23/plus/plus.csv"

FILE_HEADERS = [
    "product_url",
    "product_name",
    "product_price",
    "product_ingredients",
    "product_nutrients",
    "product_base_unit_price",
    "breadcrumb",
    "product_image",
]