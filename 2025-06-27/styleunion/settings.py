import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

PROJECT_NAME = "styleunion"
BASE_URL = "https://styleunion.in/collections/womens-tops"


HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "styleunion"
PARSE_COLLECTION = "parser"
CRAWLER_COLLECTION = "crawler"  
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"

file_name = "2025-06-27/styleunion/styleunion.csv"

FILE_HEADERS = [
    "pdp_url",
    "product_name",
    "regular_price",
    "color",
    "sku",
    "size",
    "care_instructions",
    "fabric_type",
    "rating",
    "review",
    "pattern",
    "pocket",
    "clothing_fit",
    "sleeve_type",
    "collar_type",
    "clothing_length",
    "product_description",
    "images"
]