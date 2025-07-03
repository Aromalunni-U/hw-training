import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

HEADERS = {
    "authority": "www2.hm.com",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "upgrade-insecure-requests": "1",
}

BASE_URL = "https://kuludonline.com"


PROJECT_NAME = "kuludonline"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "kuludonline"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

file_name = "2025-07-03/kuludonline/kuludonline.csv"

FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "instock",
    "discount",
    "sale_price",
    "mrp"
]