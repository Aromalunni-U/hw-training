import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

headers = {
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
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

cookies = {
        'datadome': '2mSnKqADcMbwDwWM3vW~uINMeP0cVG3X7FF5j8ZoQVzpfnJGMCXFc06a2QR4ZAl9C1WDV_MncZlsIw0VWSbO18w4skZobLB9UegmIOPNH_UqGbfC88nI_2T0O4bAp__K'
}


BASE_URL = "https://www.coop.ch/de/"

PROJECT_NAME = "coop"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "coop"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

file_name = "2025-08-11/Coop/coop.csv"

FILE_HEADERS = [
    "pdp_url",
    "product_name", 
    "product_id" ,
    "review",
    "rating",
    "breadcrumb", 
    "brand",
    "selling_price",
    "regular_price",
    "grammage_quantity",
    "grammage_unit",
    "percentage_discount",
    "country_of_origin",
    "image"
]