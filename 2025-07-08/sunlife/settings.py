import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/135.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "X-CSRF-Token": "hQDFE92su6ZT5islI3NahosY3BnPiinCFoxETXkF",
    "Referer": "https://sunlife.qa/"
}

BASE_URL = "https://sunlife.qa/"
ajax_url = "https://sunlife.qa/ajax/categoriesdropdown"


PROJECT_NAME = "sunlife"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "sunlife"
PARSE_COLLECTION = "parser"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"

file_name = "2025-07-08/sunlife/sunlife.csv"


FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "instock",
    "discount",
    "sale_price",
    "mrp"
]