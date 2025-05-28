import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_URL = "https://product-search.services.dmtech.com/si/search/static"

BASE_URL_PRODUCT = "https://products.dm.de/product/SI/products/detail/gtin/{}"

HEADERS = {
    "user-agent": "",
    "Content-Type": "application/json",
    "referer":"https://www.dm.si/"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 Chrome/95.0.4638.74 Mobile Safari/537.36",
]

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "dm"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  

file_name = "2025-05-27/dm/dm.csv"

FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "product_code",
    "product_price", 
    "currency",
    "brand",
    "images",
    "breadcrumb",
    "rating",
    "review",
    "features",
    "product_description",
    "ingredients",
    "storage_instructions",
    "warning",
    "company_address",
    "nutritional_information",
    "manufacturer_address",
    "promotion_valid_from",
    "promotion_valid_upto",
    "promotion_description",
    "percentage_discount"
]