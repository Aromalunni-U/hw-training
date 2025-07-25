import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


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

category_url = "https://www.very.co.uk/browse/kids-clothes/gender--boy"


PROJECT_NAME = "gall"

MONGO_URI = "mongodb://localhost:27017/"  
DB_NAME = "very"
DATA_COLLECTION = "parser"

file_name = "2025-07-24/Very/very.csv"

FILE_HEADERS = [
    "pdp_url",
    "product_id",
    "product_name",
    "brand",
    "currency",
    "selling_price",
    "regular_price",
    "promotion_description",
    "review",
    "rating",
    "image",
    "product_description",
    "size",
    "material_care",
    "availability"
]