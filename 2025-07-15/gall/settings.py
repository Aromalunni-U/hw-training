import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)



BASE_URL = "https://www.gall.nl"

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

PROJECT_NAME = "gall"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "gall"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

file_name = "2025-07-15/gall/gall.csv"


FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "regular_price",
    "price_was",
    "percentage_discount",
    "product_description",
    "breadcrumb",
    "rating",
    "review",
    "image",
    "alchole_percentage",
    "ingredient",
    "allergens",
    "alchol_by_volume",
    "instock",
    "nutritions"
]